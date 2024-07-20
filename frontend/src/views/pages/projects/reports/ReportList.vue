<script>
import ReportService from '@/service/ReportService';
import ReportCreateDialog from '@/components/projects/reporting/ReportCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

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
            pagination: { page: 1, limit: 20 },
            reportService: new ReportService()
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
            this.reportService
                .getReports(this.$api, this.projectId, params)
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
            this.reportService
                .getReports(this.$api, this.projectId, params)
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
            >
                <template #header>
                    <div class="grid">
                        <IconField iconPosition="left">
                            <InputIcon class="fa fa-search"></InputIcon>
                            <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                        </IconField>
                    </div>
                </template>
                <Column field="name" header="Name"> </Column>
                <Column field="template" header="Template"></Column>
                <Column field="author.username" header="Author"></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>

</template>
