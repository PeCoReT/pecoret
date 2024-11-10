<script>
import FindingTabMenu from '@/components/navigation/FindingTabMenu.vue';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import FindingAsAdvisoryDialog from '@/components/dialogs/FindingAsAdvisoryDialog.vue';
import FileDrop from '@/components/forms/fields/FileDrop.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import FindingUpdateDialog from '@/components/dialogs/FindingUpdateDialog.vue';
import { findingStatusChoices, severityChoices } from '@/utils/constants';

export default {
    name: 'FindingDetail',
    mounted() {
        this.getFinding();
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            finding: { component: {} },
            showPreview: false,
            previewData: null,
            previewLoading: false,
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'FindingList',
                        params: { projectId: this.$route.params.projectId }
                    }).path
                },
                {
                    label: 'Finding Detail',
                    disabled: true
                }
            ],
            downloadPending: false
        };
    },
    computed: {
        containerCol() {
            if (this.showPreview === true) {
                return 'col-span-6';
            }
            return 'col-span-12';
        },
        previewUrl() {
            let blob = new Blob([this.previewData], { type: 'application/pdf' });
            return URL.createObjectURL(blob);
        },
        userAccountDisplay() {
            if (this.finding.user_account && this.finding.user_account.username !== '') {
                return this.finding.user_account.username;
            }
            return '-';
        }
    },
    methods: {
        findingStatusChoices() {
            return findingStatusChoices;
        },
        severityChoices() {
            return severityChoices;
        },
        getFinding() {
            this.$api.get(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.findingId }).then((response) => {
                this.finding = response.data;
                this.breadcrumbs[this.breadcrumbs.length - 1] = {
                    label: this.finding.unique_id,
                    disabled: true
                };
            });
        },
        deleteFinding() {
            this.$api.delete(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.findingId }).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Confirmed', detail: 'Finding deleted!', life: 3000 });
                this.$router.push({ name: 'FindingList', params: { projectId: this.projectId } });
            });
        },
        patchFindingData(data) {
            this.$api
                .patch(
                    this.$api.e.pFindingDetail,
                    {
                        pPk: this.projectId,
                        pk: this.finding.pk
                    },
                    data
                )
                .then((response) => {
                    this.finding = response.data;
                    if (this.showPreview === true) {
                        this.getPreviewData();
                    }
                    this.$toast.add({ severity: 'success', summary: 'Updated', detail: 'Finding updated!', life: 3000 });
                });
        },
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this finding?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteFinding();
                }
            });
        },
        forceFileDownload(response, title) {
            let blob = new Blob([response.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', title);
            link.click();
            this.downloadPending = false;
        },
        togglePreview() {
            this.showPreview = !this.showPreview;
            if (this.showPreview === true) {
                this.getPreviewData();
            } else {
                this.previewData = null;
            }
        },
        getPreviewData() {
            this.previewLoading = true;
            let config = {
                responseType: 'arraybuffer'
            };
            this.$api
                .get(`/projects/${this.projectId}/findings/${this.findingId}/preview/`, config)
                .then((response) => {
                    this.previewData = response.data;
                })
                .finally(() => {
                    this.previewLoading = false;
                });
        },
        downloadAsPDF() {
            this.downloadPending = true;
            this.$api
                .get(
                    this.$api.e.pFindingExportPdf,
                    {
                        pPk: this.projectId,
                        fPk: this.findingId
                    },
                    null,
                    { responseType: 'arraybuffer' }
                )
                .then((response) => {
                    const filename = 'finding-' + this.finding.unique_id.toLowerCase() + '.pdf';
                    this.forceFileDownload(response, filename);
                })
                .finally(() => {
                    this.downloadPending = false;
                });
        },
        patchFindingDate(findingDate) {
            let data = { finding_date: findingDate.toISOString().split('T')[0] };
            this.patchFindingData(data);
        }
    },
    components: {
        FindingUpdateDialog,
        MarkdownEditor,
        FindingTabMenu,
        DetailCardWithIcon,
        InfoCardWithForm,
        FindingAsAdvisoryDialog,
        FileDrop
    }
};
</script>

<template>
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-6">
            <div class="flex justify-start">
                <strong class="text-lg" v-if="finding.vulnerability">{{ finding.vulnerability.name }} / {{ finding.name }}</strong>
            </div>
        </div>
        <div class="col-span-6 h-full">
            <div class="flex justify-end">
                <Button icon="fa fa-eye" outlined label="Preview" @click="togglePreview"></Button>
                <Button label="Download" outlined icon="fa fa-download" :loading="downloadPending" :disabled="downloadPending" @click="downloadAsPDF"></Button>
                <FindingAsAdvisoryDialog></FindingAsAdvisoryDialog>
                <FindingUpdateDialog :finding="finding" :project-id="projectId" @object-updated="getFinding"></FindingUpdateDialog>
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-12 mt-3 gap-4">
        <div :class="containerCol">
            <FindingTabMenu class="surface-card" :finding="finding"></FindingTabMenu>
            <div class="card border-t-0">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-12 md:col-span-4">
                        <DetailCardWithIcon title="Asset" icon="fa-crosshairs" class="bg-surface-950" :text="finding.component.display_name"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-4">
                        <DetailCardWithIcon title="User Account" icon="fa-user" class="bg-surface-950" :text="userAccountDisplay"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-4">
                        <DetailCardWithIcon title="Status" icon="fa-bookmark" class="bg-surface-950" :text="finding.status"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid mt-3 grid-cols-12 gap-3">
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950 w-full" title="Status" icon="fa-bookmark">
                            <Select v-model="finding.status" :options="findingStatusChoices()" optionValue="value" @change="patchFindingData({ status: finding.status })" optionLabel="title" class="w-full"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950" title="Finding Date" icon="fa-calendar">
                            <DatePicker v-model="finding.finding_date" @update:modelValue="patchFindingDate" dateFormat="yy-mm-dd"></DatePicker>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950" title="Severity" icon="fa fa-shield-halved">
                            <Select v-model="finding.severity" :options="severityChoices()" optionLabel="label" @change="patchFindingData({ severity: finding.severity })" optionValue="value"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950" title="Needs review?" icon="fa-user-tag">
                            <ToggleSwitch v-model="finding.needs_review" @change="patchFindingData({ needs_review: finding.needs_review })"></ToggleSwitch>
                        </InfoCardWithForm>
                    </div>
                </div>

                <div class="grid gap-4 mt-3">
                    <div class="col-span-12">
                        <label>Proof</label>
                        <MarkdownEditor v-model="finding.proof_text"></MarkdownEditor>
                    </div>
                    <div class="col-span-12">
                        <FileDrop></FileDrop>
                    </div>
                    <div class="col-span-12">
                        <Button label="Save" @click="patchFindingData({ proof_text: finding.proof_text })"></Button>
                    </div>
                </div>
            </div>
        </div>

        <div :class="containerCol">
            <ProgressBar v-if="!this.previewData && this.showPreview === true" mode="indeterminate" class="h-1"></ProgressBar>
            <iframe :src="this.previewUrl" v-if="previewLoading !== true && this.previewData" class="w-full h-full" :key="previewData"></iframe>
        </div>
    </div>
</template>
