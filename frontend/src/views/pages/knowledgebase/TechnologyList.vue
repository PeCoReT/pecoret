<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import Search from '@/views/pages/attack_surface/Search.vue';
import SearchField from '@/partials/common/SearchField.vue';
import { Button } from '@/components/ui/button';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import { Badge } from '@/components/badge';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';
import { DataTable } from '@/components/datatable';

export default {
    name: 'TechnologyList',
    mixins: [listViewMixin],
    components: {
        Paginator,
        DataTable,
        Badge,
        SortListDropdownMenu,
        SearchField,
        Search,
        DataViewListLayout,
        Button
    },
    data() {
        return {
            loading: false,
            selection: {},
            items: [],
            columns: [
                {
                    key: 'name',
                    title: 'Name'
                },
                {
                    key: 'cpe',
                    title: 'CPE'
                },
                {
                    key: 'date_updated',
                    title: 'Date Updated'
                },
                {
                    key: 'source_code_available',
                    title: 'Source?'
                }
            ],
            filters: {
                search: { value: null },
                ordering: { value: null }
            }
        };
    },
    methods: {
        async bulkDelete() {
            this.$confirm.require({
                accept: async () => {
                    let itemsDeleted = 0;
                    let totalLength = Object.entries(this.selection).length;
                    for (const [key, value] of Object.entries(this.selection)) {
                        itemsDeleted++;
                        if (value === true) {
                            await this.$api
                                .delete(this.$api.e.technologyDetail, {
                                    pk: key
                                })
                                .then(() => {
                                    if (itemsDeleted === totalLength) {
                                        this.selection = {};
                                        this.getItems();
                                    }
                                });
                        }
                    }
                }
            });
        },
        commonSortFilter() {
            return commonSortFilter;
        },
        getItems(params) {
            this.loading = true;

            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.technologyList, null, data)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        search(query) {
            this.getItems({ search: query });
        }
    },
    mounted() {
        this.getItems();
    }
};
</script>

<template>
    <DataViewListLayout>
        <DataTable :loading="loading" :totalRecords="totalRecords" v-model:selection="selection" :show-bulk-select="true" :columns="columns" :items="items">
            <template #filters>
                <SortListDropdownMenu v-model="filters.ordering.value" @update:model-value="getItems" :items="commonSortFilter()"></SortListDropdownMenu>
            </template>
            <template #bulk>
                <Button @click="bulkDelete" variant="destructive">Delete</Button>
            </template>

            <template #cell="{ item, col }">
                <a v-if="col.key === 'name'" :href="this.$router.resolve({ name: 'TechnologyUpdate', params: { techId: item.pk } }).href" class="hover:underline">{{ item.name }}</a>
                <span v-else>{{ item[col.key] }}</span>
            </template>
        </DataTable>

        <template #search>
            <SearchField v-model="filters.search.value" @search="search"></SearchField>
        </template>
        <template #create-button>
            <Button :href="this.$router.resolve({ name: 'TechnologyCreate' }).href" as="a"
                ><i class="fa fa-plus"></i>
                Technology
            </Button>
        </template>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
