<script>
import ReportService from '@/service/ReportService';
import ReportTabMenu from '../../../../components/pages/ReportTabMenu.vue';
import VersionHistoryCreateDialog from '../../../../components/dialogs/VersionHistoryCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';

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
        onSort(event) {},
        onFilter(event) {},
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
            this.reportService.deleteChangeHistoryItem(this.$api, this.projectId, this.reportId, versionId).then((response) => {
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
    components: { ReportTabMenu, VersionHistoryCreateDialog, BlankSlate }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <VersionHistoryCreateDialog @object-created="getItems"></VersionHistoryCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <ReportTabMenu class="surface-card"></ReportTabMenu>

            <div class="card border-noround-top">
                <DataTable paginator lazy dataKey="pk" :value="items" :rows="pagination.limit" :totalRecords="totalRecords" filterDisplay="menu" :loading="loading" @page="onPage" @sort="onSort" :rowHover="items.length > 0" @filter="onFilter">
                    <template #empty>
                        <BlankSlate icon="fa fa-clock-rotate-left" title="Version History" text="No version history found!"></BlankSlate>
                    </template>
                    <Column field="version" header="Version"></Column>
                    <Column field="change" header="Change"></Column>
                    <Column field="date" header="Date"></Column>
                    <Column field="user.username" header="User"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>