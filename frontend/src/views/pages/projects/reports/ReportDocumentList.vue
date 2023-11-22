<script>
import ReportService from '@/service/ReportService';
import ReportTabMenu from '../../../../components/pages/ReportTabMenu.vue';
import ReportDocumentCreateDialog from '../../../../components/dialogs/ReportDocumentCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'ReportDocumentList',
    data() {
        return {
            loading: false,
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            reportService: new ReportService(),
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
            this.timerPreviewDocument = setInterval(this.getPreviewReportDocument, 5 * 1000);
        },
        cancelAutpUpdatePreviewDocument() {
            clearInterval(this.timerPreviewDocument);
            this.timerPreviewDocument = '';
        },
        cancelAutoUpdate() {
            clearInterval(this.timer);
            this.timer = '';
        },
        onSort() {},
        onFilter() {},
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
            this.reportService.getPreviewReportDocument(this.$api, this.projectId, this.reportId).then((response) => {
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
            console.log('reloading...');
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.reportService
                .getReportDocuments(this.$api, this.projectId, this.reportId, params)
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
        forceFileDownload(response, title) {
            const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', title);
            document.body.appendChild(link);
            link.click();
        },
        downloadDocument(documentId, isPreview) {
            if (isPreview === true) {
                this.previewDownloadLoading = true;
            }
            let url = '/projects/' + this.projectId + '/reports/' + this.reportId + '/report-releases/' + documentId + '/download/';
            let config = {};
            config.responseType = 'arraybuffer';
            this.$api
                .get(url, config)
                .then((response) => {
                    let filename = response.headers['content-disposition'].split('filename=')[1].split(';')[0];
                    this.forceFileDownload(response, filename);
                })
                .finally(() => {
                    this.previewDownloadLoading = false;
                });
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
            this.reportService.createReportDocument(this.$api, this.projectId, this.reportId, data).then((response) => {
                this.getPreviewReportDocument();
            });
        },
        deleteDocument(documentId) {
            this.reportService.deleteReportDocument(this.$api, this.projectId, this.reportId, documentId).then((response) => {
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
    components: { ReportTabMenu, ReportDocumentCreateDialog, BlankSlate }
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
                <ReportDocumentCreateDialog @object-created="getItems"></ReportDocumentCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <ReportTabMenu class="surface-card"></ReportTabMenu>
            <div class="card border-noround-top">
                <div class="grid">
                    <div class="col-6"></div>
                    <div class="col-6">
                        <div class="flex justify-content-end">
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
                <div class="grid" v-if="this.previewDocument !== null">
                    <div class="col-6 col-offset-6">
                        <div class="flex justify-content-end">
                            <small>Created at {{ this.previewDocument.date_created }}</small>
                        </div>
                    </div>
                </div>
                <DataTable paginator lazy :rowHover="items.length > 0" dataKey="pk" :totalRecords="totalRecords" filterDisplay="menu" :rows="pagination.limit" :value="items" :loading="loading" @page="onPage" @sort="onSort" @filter="onFilter">
                    <template #empty>
                        <BlankSlate icon="fa fa-file" title="Report documents" text="No report documents found!"></BlankSlate>
                    </template>
                    <Column field="name" header="Header"></Column>
                    <Column field="release_type" header="Release Type"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-download" :loading="getDocumentLoadingIndicator(slotProps.data)" :disabled="!slotProps.data.task" label="Download" @click="downloadDocument(slotProps.data.pk)"></Button>
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>