<script>
import ProjectService from '@/service/ProjectService';
import ProjectFileCreateDialog from '@/components/dialogs/ProjectFileCreateDialog.vue';
import forceFileDownload from '@/utils/file';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'ProjectFileList',
    components: { GenericDataTable, BaseListLayout, ProjectFileCreateDialog },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Project Files',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            service: new ProjectService()
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
            this.service
                .getProjectFiles(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        downloadFile(file_id) {
            this.service.downloadProjectFile(this.$api, this.projectId, file_id).then((response) => {
                forceFileDownload(response);
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Dou you want to delete this file?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteProjectFile(this.$api, this.projectId, id).then(() => {
                        this.getItems();
                    });
                }
            });
        }
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ProjectFileCreateDialog @object-created="this.getItems"></ProjectFileCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No project files found!"
                blank-slate-title="No Project Files!"
                blank-slate-icon="fa fa-file"
                :model-value="items"
                @page="onPage"
            >
                <Column field="name" header="Name"></Column>

                <Column field="date_created" header="Date created"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-download" @click="downloadFile(slotProps.data.pk)"></Button>
                        <Button size="small" outlined severity="danger" icon="fa fa-trash" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
