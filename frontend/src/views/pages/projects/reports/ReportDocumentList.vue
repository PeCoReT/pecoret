<script>
import { ReportDocumentCreateDialog, ReportTabMenu } from '@/partials/projects';
import { BlankSlate } from '@/components/blankslate';
import forceFileDownload from '@/utils/file';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Select } from '@/components/select';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { Paginator } from '@/components/paginator';

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
            previewDocument: {}
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
        commonSortFilter() {
            return commonSortFilter;
        },
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
        onPage(page) {
            this.pagination.page = page;
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
                    this.$toaster({
                        title: 'Deleted',
                        description: 'Document was deleted!',
                        duration: 3000
                    });
                    this.getItems();
                });
        }
    },
    components: {
        Paginator,
        ContainerLayout,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        ReportTabMenu,
        ReportDocumentCreateDialog,
        BlankSlate,
        Button,
        Select
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <ReportTabMenu class="md:max-w-lg"></ReportTabMenu>
        </template>
        <template #right-header>
            <ReportDocumentCreateDialog @object-created="getItems"></ReportDocumentCreateDialog>
        </template>
        <div class="grid grid-cols-12">
            <div class="col-span-6">
                <span v-if="this.previewDocument && this.previewDocument.pk">{{ this.getDocumentStatus(this.previewDocument) }}</span>
            </div>
            <div class="col-span-6">
                <div class="flex justify-end">
                    <Button :disabled="!previewDocument.pk" :loading="previewDownloadLoading" class="mr-2" variant="outline" @click="downloadDocument(previewDocument.pk, true)"><i class="fa fa-download" /> Download </Button>
                    <Button
                        :disabled="this.previewDocument.task && !this.previewDocument.task.stopped && this.previewDocument.task.hasOwnProperty('stopped')"
                        :loading="getDocumentLoadingIndicator(this.previewDocument)"
                        outlined
                        @click="createPreviewDocument"
                    >
                        <i class="fa fa-rotate"></i> Preview Document
                    </Button>
                </div>
            </div>
        </div>
        <div v-if="this.previewDocument !== null" class="grid mt-3">
            <div class="col-span-6 col-offset-6">
                <div class="flex justify-end">
                    <small v-if="this.previewDocument && this.previewDocument.pk">Created at {{ this.previewDocument.date_created }}</small>
                </div>
            </div>
        </div>

        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <SortListDropdownMenu :items="commonSortFilter()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-file" blank-slate-text="No report documents found!" blank-slate-title="No Report Documents!">
            <template #item="{ item }">
                <div class="flex-1">
                    {{ item.name }}
                    <div class="flex text-xs text-muted-foreground">{{ item.release_type }}</div>
                </div>
                <div class="flex-1">
                    {{ this.getDocumentStatus(item) }}
                </div>
                <div class="flex gap-2">
                    <Button :disabled="!item.task" :loading="getDocumentLoadingIndicator(item)"  @click="downloadDocument(item.pk)">
                        <i class="fa fa-download"></i>
                        Download
                    </Button>
                    <Button variant="destructive" @click="confirmDialogDelete(item.pk)">
                        <i class="fa fa-trash"></i>
                    </Button>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </ContainerLayout>
</template>
