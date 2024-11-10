<script>
import CompanyCreateDialog from '@/components/dialogs/CompanyCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'CompanyList',
    data() {
        return {
            breadcrumbs: [{ label: 'Companies', disabled: true }],
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 }
        };
    },
    mounted() {
        this.getCompanies();
    },
    methods: {
        onGlobalSearch(query) {
            let params = {
                search: query
            };
            this.$api
                .get(this.$api.e.companyList, null, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => (this.loading = false));
        },
        getCompanies() {
            this.loading = true;
            let data = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.$api
                .get(this.$api.e.companyList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onRowClick(row) {
            this.$router.push({
                name: 'CompanyDetail',
                params: {
                    companyId: row.data.pk
                }
            });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getCompanies();
        }
    },
    components: { GenericDataTable, BaseListLayout, CompanyCreateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <CompanyCreateDialog @object-created="getCompanies"></CompanyCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No companies found!"
                blank-slate-title="No Companies!"
                blank-slate-icon="fa fa-globe"
                :model-value="items"
                @page="onPage"
                @rowClick="onRowClick"
                :show-search="true"
                @search="onGlobalSearch"
            >
                <Column field="name" header="Name"></Column>
                <Column field="street" header="Street"></Column>
                <Column field="city" header="City"></Column>
                <Column field="country" header="Country"></Column>
                <Column field="report_template" header="Report Template"></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
