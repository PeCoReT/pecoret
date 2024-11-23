<script>
import ReportCreateDialog from '@/components/projects/reporting/ReportCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'ReportList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Reports',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 }
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.$api
                .get(this.$api.e.pReportList, { pPk: this.projectId }, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onGlobalSearch(query) {
            let params = {
                search: query
            };
            this.$api
                .get(this.$api.e.pReportList, { pPk: this.projectId }, params)
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
                name: 'ReportDetail',
                params: {
                    projectId: this.projectId,
                    reportId: row.data.pk
                }
            });
        }
    },
    components: { GenericDataTable, BaseListLayout, ReportCreateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ReportCreateDialog @object-created="getItems"></ReportCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No reports found!"
                blank-slate-title="No Reports!"
                blank-slate-icon="fa fa-file"
                :model-value="items"
                @rowClick="onRowClick"
                @page="onPage"
                @search="onGlobalSearch"
                :show-search="true"
            >
                <Column field="name" header="Name"></Column>
                <Column field="template" header="Template"></Column>
                <Column field="date_created" header="Date Created"></Column>
                <Column field="date_updated" header="Date Updated"></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
