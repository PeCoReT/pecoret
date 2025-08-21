<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import { Button } from '@/components/ui/button';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';
import DataTable from '@/components/datatable/DataTable.vue';

export default {
    name: 'CompanyList',
    mixins: [listViewMixin],
    data() {
        return {
            items: [],
            loading: false,
            filters: {
                search: { value: null },
                ordering: { value: null }
            },
            commonSortFilter: commonSortFilter
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.companyList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                        this.loading = false;
                });
        }
    },
    components: {
        Paginator,
        DataTable,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        DataViewListLayout,
        Button
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>
        <template #create-button>
            <Button :href="this.$router.resolve({ name: 'CompanyCreate' }).href" as="a"><i class="fa fa-plus" /> Company </Button>
        </template>
        <DataTable
            :columns="[
                { key: 'name', title: 'Name' },
                { key: 'city', title: 'City' },
                { key: 'country', title: 'Country' },
                { key: 'report_template', title: 'Template' }
            ]"
            :totalRecords="totalRecords"
            :items="items"
            :loading="loading"
        >
            <template #filters>
                <SortListDropdownMenu :items="commonSortFilter" v-model="filters.ordering.value" @update:model-value="getItems()"></SortListDropdownMenu>
            </template>
            <template #cell="{ item, col }">
                <span v-if="col.key === 'name'">
                    <a :href="this.$router.resolve({ name: 'CompanyDetail', params: { companyId: item.pk } }).href" class="hover:underline">{{ item.name }}</a>
                </span>
                <span v-else>{{ item[col.key] }}</span>
            </template>
        </DataTable>

        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
