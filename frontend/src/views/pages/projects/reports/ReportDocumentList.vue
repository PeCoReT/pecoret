<script>
import ReportTabMenu from '@/components/projects/reporting/ReportTabMenu.vue';
import ReportDocumentCreateDialog from '@/components/dialogs/ReportDocumentCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import forceFileDownload from "@/utils/file";

export default {
    name: 'ReportDocumentList',
    data() {
        return {
            loading: false,
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            pagination: { page: 1, limit: 20 },
            totalRecords: 0,
            timer: '',
            timerPreviewDocument: '',
            items: [],
            previewDownloadLoading: false,
            previewDocument: {},
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
                    label: 'Documents',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getItems();
        this.getPreviewReportDocument();
    },
    beforeUnmount() {
        this.cancelAutoUpdate();
    },
    methods: {
        startAutoUpdate() {
            // reload data every 5s
            this.timer = setInterval(this.getItems, 5 * 1000);
        },
        startAutoUpdatePreviewDocument() {
            this.timerPreviewDocument = setInterval(this.getPreviewReportDocument, 3 * 1000);
        },
        cancelAutpUpdatePreviewDocument() {
            clearInterval(this.timerPreviewDocument);
            this.timerPreviewDocument = '';
        },
        cancelAutoUpdate() {
            clearInterval(this.timer);
            this.timer = '';
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getDocumentLoadingIndicator(document) {
            if (!document.task) {
                // return false, but this will make the button disabled!
                return false;
            }
            if (!document.task.started) {
                return true;
            }
            if (document.task.stopped) {
                return false;
            }
            return true;
        },
        getPreviewReportDocument() {
            this.$api
                .get(this.$api.e.pReportPreviewDocument, {
                    pPk: this.projectId,
                    rPk: this.reportId
                })
                .then((response) => {
                    this.previewDocument = response.data;
                    if (this.previewDocumentInProgress() === true) {
                        if (this.timerPreviewDocument === '') {
                            this.startAutoUpdatePreviewDocument();
                        }
                    } else {
                        this.cancelAutpUpdatePreviewDocument();
                    }
                });
        },
        previewDocumentInProgress() {
            // check if previewDocument is currently created
            if (this.previewDocument.task_id && !this.previewDocument.task.started) {
                return true;
            }
            if (this.previewDocument.task && this.previewDocument.task.started && !this.previewDocument.task.stopped) {
                return true;
            }
            return false;
        },
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.$api
                .get(this.$api.e.pReportDocumentList, { pPk: this.projectId, rPk: this.reportId }, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                    let timerRequired = false;
                    this.items.forEach((item) => {
                        if (item.task_id && !item.task.started) {
                            timerRequired = true;
                        }
                        if (item.task && item.task.started && !item.task.stopped) {
                            timerRequired = true;
                        }
                    });
                    if (timerRequired === true) {
                        if (this.timer === '') {
                            this.startAutoUpdate();
                        }
                    } else {
                        this.cancelAutoUpdate();
                    }
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        downloadDocument(documentId, isPreview) {
            if (isPreview === true) {
                this.previewDownloadLoading = true;
            }
            let config = {
                responseType: 'arraybuffer'
            };
            this.$api
                .get(
                    this.$api.e.pReportDocumentPdf,
                    {
                        pPk: this.projectId,
                        rPk: this.reportId,
                        pk: documentId
                    },
                    null,
                    config
                )
                .then((response) => {
                    forceFileDownload(response);
                })
                .finally(() => {
                    this.previewDownloadLoading = false;
                });
        },
        getDocumentStatus(document) {
            if (document.task && !document.task.started && document.task_id) {
                return 'Status: Scheduled...';
            } else if (document.task && document.task.success === true) {
                return 'Status: Document built successfully!';
            } else if (document.task && document.task.success === false) {
                return 'Status: Failed building document!';
            } else {
                return 'Status: Unknown!';
            }
        },
        confirmDialogDelete(documentId) {
            this.$confirm.require({
                message: 'Do you want to delete this document?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteDocument(documentId);
                }
            });
        },
        createPreviewDocument() {
            let data = { name: 'Preview', release_type: 'Preview' };
            this.$api
                .post(
                    this.$api.e.pReportDocumentList,
                    {
                        pPk: this.projectId,
                        rPk: this.reportId
                    },
                    data
                )
                .then(() => {
                    this.getPreviewReportDocument();
                });
        },
        deleteDocument(documentId) {
            this.$api
                .delete(this.$api.e.pReportDocumentDetail, {
                    pPk: this.projectId,
                    rPk: this.reportId,
                    pk: documentId
                })
                .then(() => {
                    this.$toast.add({
                        severity: 'info',
                        summary: 'Deleted',
                        detail: 'Document was deleted!',
                        life: 3000
                    });
                    this.getItems();
                });
        }
    },
    components: { GenericDataTable, ReportTabMenu, ReportDocumentCreateDialog, BlankSlate }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-6"></div>
        <div class="col-span-6">
            <div class="flex justify-end">
                <ReportDocumentCreateDialog @object-created="getItems"></ReportDocumentCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid mt-3">
        <div class="col-span-12">
            <ReportTabMenu></ReportTabMenu>
            <div class="card border-noround-top">
                <div class="grid grid-cols-12">
                    <div class="col-span-6">
                        <span v-if="this.previewDocument && this.previewDocument.pk">{{ this.getDocumentStatus(this.previewDocument) }}</span>
                    </div>
                    <div class="col-span-6">
                        <div class="flex justify-end">
                            <Button label="Download" icon="fa fa-download" class="mr-2" :disabled="!previewDocument.pk" outlined @click="downloadDocument(previewDocument.pk, true)" :loading="previewDownloadLoading"></Button>
                            <Button
                                label="Preview Document"
                                icon="fa fa-plus"
                                outlined
                                :loading="getDocumentLoadingIndicator(this.previewDocument)"
                                :disabled="this.previewDocument.task && !this.previewDocument.task.stopped"
                                @click="createPreviewDocument"
                            ></Button>
                        </div>
                    </div>
                </div>
                <div class="grid mt-3" v-if="this.previewDocument !== null">
                    <div class="col-span-6 col-offset-6">
                        <div class="flex justify-end">
                            <small v-if="this.previewDocument && this.previewDocument.pk">Created at {{ this.previewDocument.date_created }}</small>
                        </div>
                    </div>
                </div>
                <GenericDataTable
                    :total-records="totalRecords"
                    :loading="loading"
                    :pagination="pagination"
                    blank-slate-text="No report documents found!"
                    blank-slate-title="No Report Documents!"
                    blank-slate-icon="fa fa-file"
                    :model-value="items"
                    @page="onPage"
                >
                    <Column field="name" header="Header"></Column>
                    <Column field="release_type" header="Release Type"></Column>
                    <Column header="Status">
                        <template #body="slotProps">
                            {{ this.getDocumentStatus(slotProps.data) }}
                        </template>
                    </Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-download" :loading="getDocumentLoadingIndicator(slotProps.data)" :disabled="!slotProps.data.task" label="Download" @click="downloadDocument(slotProps.data.pk)"></Button>
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </GenericDataTable>
            </div>
        </div>
    </div>
</template>
