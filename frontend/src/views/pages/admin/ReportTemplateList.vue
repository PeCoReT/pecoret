<script>
import AdminService from '@/service/AdminService';
import ReportTemplateUpdateDialog from '../../../components/dialogs/ReportTemplateUpdateDialog.vue';
import ReportTemplateCreateDialog from '../../../components/dialogs/ReportTemplateCreateDialog.vue';

export default {
    name: 'ReportTemplateList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Report Templates',
                    disabled: true
                }
            ],
            service: new AdminService(),
            loading: false,
            pagination: { page: 1, limit: 20 },
            totalRecords: 0,
            items: []
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
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.service
                .getReportTemplates(this.$api, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to delete this report template?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteReportTemplate(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: 'success',
                            summary: 'Deleted',
                            detail: 'Report template was deleted successfully!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    },
    components: { ReportTemplateUpdateDialog, ReportTemplateCreateDialog }
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
            <div class="justify-content-start flex"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <ReportTemplateCreateDialog @object-created="getItems"></ReportTemplateCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <Card>
                <template #content>
                    <DataTable paginator rowHover :rows="pagination.limit" :value="items" lazy filterDisplay="menu" :totalRecords="totalRecords" :loading="loading" @page="onPage" responsiveLayout="scroll" @filter="onFilter" @sort="onSort">
                        <Column field="name" header="Name"></Column>
                        <Column field="package" header="Package"></Column>
                        <Column field="status" header="Status"></Column>
                        <Column header="Actions">
                            <template #body="slotProps">
                                <ReportTemplateUpdateDialog :template="slotProps.data"></ReportTemplateUpdateDialog>
                                <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                            </template>
                        </Column>
                    </DataTable>
                </template>
            </Card>
        </div>
    </div>
</template>