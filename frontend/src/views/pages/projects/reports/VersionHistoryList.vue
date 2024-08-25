<script>
import ReportService from '@/service/ReportService';
import ReportTabMenu from '@/components/projects/reporting/ReportTabMenu.vue';
import VersionHistoryCreateDialog from '@/components/dialogs/VersionHistoryCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'VersionHistoryList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Reports',
                    to: this.$router.resolve({
                        name: 'ReportList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Report Detail',
                    to: this.$router.resolve({
                        name: 'ReportDetail',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                },
                {
                    label: 'Version History',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
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
                .getVersionHistoryItems(this.$api, this.projectId, this.reportId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(versionId) {
            this.$confirm.require({
                message: 'Do you want to delete this change?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteChangeHistoryItem(versionId);
                }
            });
        },
        deleteChangeHistoryItem(versionId) {
            this.reportService.deleteChangeHistoryItem(this.$api, this.projectId, this.reportId, versionId).then(() => {
                this.$toast.add({
                    severity: 'info',
                    summary: 'Deleted',
                    detail: 'Change was deleted!',
                    life: 3000
                });
                this.getItems();
            });
        }
    },
    components: { GenericDataTable, BaseListLayout, ReportTabMenu, VersionHistoryCreateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <VersionHistoryCreateDialog @object-created="getItems"></VersionHistoryCreateDialog>
        </template>

        <template #default>
            <ReportTabMenu class="surface-card"></ReportTabMenu>

            <div class="card border-noround-top">
                <GenericDataTable
                    :total-records="totalRecords"
                    :loading="loading"
                    :pagination="pagination"
                    blank-slate-text="No version history found!"
                    blank-slate-title="No Version History!"
                    blank-slate-icon="fa fa-clock-rotate-left"
                    :model-value="items"
                >
                    <Column field="version" header="Version"></Column>
                    <Column field="change" header="Change"></Column>
                    <Column field="date" header="Date"></Column>
                    <Column field="user.username" header="User"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </GenericDataTable>
            </div>
        </template>
    </BaseListLayout>
</template>
