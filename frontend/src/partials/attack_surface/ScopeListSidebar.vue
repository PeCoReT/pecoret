<script>
import SearchField from '@/partials/common/SearchField.vue';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';
import { Button } from '@/components/ui/button';

export default {
    name: 'ScopeListSidebar',
    components: { Button, Paginator, SearchField },
    emits: ['sidebarChanged', 'update:shouldReload'],
    props: {
        program: {
            required: true
        },
        shouldReload: {
            required: false,
            default: false
        }
    },
    mixins: [listViewMixin],
    data() {
        return {
            items: [],
            reload: this.shouldReload,
            selectedItem: null,
            filters: {
                search: { value: null },
                program: { value: this.program }
            }
        };
    },
    methods: {
        sidebarChanged(item) {
            this.selectedItem = item;
            this.$emit('sidebarChanged', item);
        },
        getItems(params) {
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api.get(this.$api.e.asScopeList, null, data).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        deleteScope(pk) {
            this.$confirm.require({
                accept: () => {
                    this.$api.delete(this.$api.e.asScopeDetail, { pk: pk }).then(() => {
                        this.getItems();
                        this.selectedItem = null;
                    });
                }
            });
        },
        onReload(value) {
            if (value && value === true) {
                this.selectedItem = null;
                this.getItems();
                this.$emit('update:shouldReload', false);
            }
        }
    },
    watch: {
        program: {
            immediate: true,
            handler(value) {
                if (!value) {
                    this.items = [];
                    this.totalRecords = 0;
                } else {
                    this.filters.program.value = value;
                    this.getItems();
                }
            }
        },
        shouldReload: {
            immediate: true,
            handler(value) {
                this.onReload(value);
            }
        }
    }
};
</script>

<template>
    <div class="bg-card rounded-lg p-1 w-full border">
        <SearchField v-model="filters.search.value" @search="onSearch" :disabled="program === null"></SearchField>
        <ul class="space-y-1 mt-1">
            <li v-if="program" v-for="item in items" :key="item.pk" :class="{ 'bg-muted': selectedItem && selectedItem.pk === item.pk }" class="p-2 rounded hover:bg-accent hover:cursor-pointer" @click="sidebarChanged(item)">
                <div class="flex flex-row items-center">
                    <div class="flex flex-grow">
                        {{ item.name }}
                    </div>
                    <div class="flex justify-end">
                        <Button size="small" variant="destructive" class="p-1 px-2" @click="deleteScope(item.pk)"> Delete </Button>
                    </div>
                </div>
            </li>
            <li v-if="items.length < 1 || !program" class="p-2 rounded">No available options</li>
        </ul>
    </div>
    <Paginator :rows="pagination.limit" :totalRecords="totalRecords" class="mt-3 flex justify-center" @page="onPage"> </Paginator>
</template>

<style scoped></style>
