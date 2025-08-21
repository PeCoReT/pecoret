<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Badge } from '@/components/badge';
import { Button } from '@/components/ui/button';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';
import { paramMixin } from '@/mixins/params';

export default {
    name: 'ProgramList',
    components: {
        Paginator,
        Badge,
        DataViewContent,
        DataViewHeader,
        SortListDropdownMenu,
        SearchField,
        DataViewListLayout,
        Button
    },
    mixins: [listViewMixin, paramMixin],
    data() {
        return {
            items: [],
            loading: false,
            filters: {
                ordering: { value: '-date_created' },
                search: { value: null }
            },
            sortItems: commonSortFilter,
            selection: {}
        };
    },
    mounted() {
        this.initFromUrl();
        this.getItems();
    },
    methods: {
        async bulkDeleteCallback(key, value) {
            return this.$api.delete(this.$api.e.asProgramDetail, { pk: key })
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asProgramList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>
        <template #create-button>
            <Button :href="this.$router.resolve({ name: 'AttackSurfaceProgramCreate' }).href" as="a"><i
                    class="fa fa-plus" /> Program </Button>
        </template>
        <DataViewHeader :total-records="totalRecords" v-model:selection="selection" v-model:items="items"
            :show-bulk-select="true">
            <template #filters>
                <SortListDropdownMenu :items="sortItems" v-model="filters.ordering.value"
                    @update:model-value="this.getItems()"></SortListDropdownMenu>
            </template>
            <template #bulk>
                <Button @click="bulkDelete(this.bulkDeleteCallback)" variant="destructive">
                    <i class="fa fa-trash"></i> Delete</Button>
            </template>
        </DataViewHeader>
        <DataViewContent v-model:items="items" :loading="loading" blank-slate-icon="fa fa-shield"
            blank-slate-text="No programs found!" blank-slate-title="No Programs!" :show-bulk-select="true"
            v-model:selection="selection">
            <template #item="{ item }">
                <div class="flex-1">
                    <div class="flex justify-between items-center">
                        <div class="font-semibold text-base">
                            <a :href="this.$router.resolve({ name: 'AttackSurfaceProgramUpdate', params: { programId: item.pk } }).href"
                                class="hover:underline">
                                {{ item.name }}
                            </a>
                        </div>
                    </div>

                    <div class="flex flex-wrap">
                        <span v-for="tag in item.tags" :key="tag.pk"
                            class="bg-background text-accent-foreground text-sm px-2 py-1 rounded border border-gray-800 hover:bg-surface-800 hover:cursor-pointer">
                            {{ tag.name }}
                        </span>
                    </div>

                    <div class="text-xs text-gray-500 mt-2">
                        <span> ID: {{ item.pk }} </span>
                        <span class="mx-2">|</span>
                        <span>
                            Created: <span class="font-medium">{{ item.date_created }}</span>
                        </span>
                        <span class="mx-2">|</span>
                        <span>
                            Updated: <span class="font-medium">{{ item.date_updated }}</span>
                        </span>
                    </div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
