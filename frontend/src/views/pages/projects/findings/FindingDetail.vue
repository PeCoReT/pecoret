<script>
import FindingService from '@/service/FindingService';
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import FindingAsAdvisoryDialog from '@/components/dialogs/FindingAsAdvisoryDialog.vue';
import FileDrop from '@/components/elements/forms/FileDrop.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import FindingUpdateDialog from '@/components/projects/findings/FindingUpdateDialog.vue';

export default {
    name: 'FindingDetail',
    mounted() {
        this.getFinding();
    },
    data() {
        return {
            service: new FindingService(),
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
            severityOptions: [
                { label: 'Critical', value: 'Critical' },
                { label: 'High', value: 'High' },
                { label: 'Medium', value: 'Medium' },
                { label: 'Low', value: 'Low' },
                { label: 'Informational', value: 'Informational' }
            ],
            statusChoices: [
                { title: 'Open', value: 'Open' },
                { title: 'Fixed', value: 'Fixed' },
                { title: "Won't Fix", value: 'Wont Fix' }
            ],
            downloadPending: false
        };
    },
    computed: {
        containerCol() {
            if (this.showPreview === true) {
                return 'col-6';
            }
            return 'col-12';
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
        getFinding() {
            this.service.getFinding(this.projectId, this.findingId).then((response) => {
                this.finding = response.data;
                this.breadcrumbs[this.breadcrumbs.length - 1] = {
                    label: this.finding.unique_id,
                    disabled: true
                };
            });
        },
        deleteFinding() {
            this.service.deleteFinding(this.$api, this.projectId, this.findingId).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Confirmed', detail: 'Finding deleted!', life: 3000 });
                this.$router.push({ name: 'FindingList', params: { projectId: this.projectId } });
            });
        },
        patchFindingData(data) {
            this.service.patchFinding(this.$api, this.projectId, this.findingId, data).then((response) => {
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
                .get('/projects/' + this.projectId + '/findings/' + this.findingId + '/preview/', config)
                .then((response) => {
                    this.previewData = response.data;
                })
                .finally(() => {
                    this.previewLoading = false;
                });
        },
        downloadAsPDF() {
            this.downloadPending = true;
            this.service
                .downloadAsPDF(this.$api, this.projectId, this.findingId)
                .then((response) => {
                    const filename = 'finding-' + this.finding.unique_id.toLowerCase() + '.pdf';
                    this.forceFileDownload(response, filename);
                })
                .finally(() => {
                    this.downloadPending = false;
                });
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
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start">
                <strong class="text-lg" v-if="finding.vulnerability">{{ finding.vulnerability.name }} / {{ finding.name }}</strong>
            </div>
        </div>
        <div class="col-6 h-full">
            <div class="flex justify-content-end">
                <Button icon="fa fa-eye" outlined label="Preview" @click="togglePreview"></Button>
                <Button label="Download" outlined icon="fa fa-download" :loading="downloadPending" :disabled="downloadPending" @click="downloadAsPDF"></Button>
                <FindingAsAdvisoryDialog></FindingAsAdvisoryDialog>
                <FindingUpdateDialog :finding="finding" :project-id="projectId" @object-updated="getFinding"></FindingUpdateDialog>
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>

    <div class="grid">
        <div :class="containerCol">
            <FindingTabMenu class="surface-card" :finding="finding"></FindingTabMenu>
            <div class="card border-noround-top">
                <div class="grid">
                    <div class="col-12 md:col-4">
                        <DetailCardWithIcon title="Asset" icon="fa-crosshairs" class="surface-ground" :text="finding.component.display_name"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-4">
                        <DetailCardWithIcon title="User Account" icon="fa-user" class="surface-ground" :text="userAccountDisplay"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-4">
                        <DetailCardWithIcon title="Status" icon="fa-bookmark" class="surface-ground" :text="finding.status"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid">
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Status" icon="fa-bookmark">
                            <Dropdown v-model="finding.status" :options="statusChoices" optionValue="value" @change="patchFindingData({ status: finding.status })" optionLabel="title" class="w-full"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground" title="Finding Date" icon="fa-calendar">
                            <Calendar v-model="finding.finding_date" @change="patchFindingData({ finding_date: finding.finding_date })"></Calendar>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground" title="Severity" icon="fa fa-shield-halved">
                            <Dropdown v-model="finding.severity" :options="severityOptions" optionLabel="label" @change="patchFindingData({ severity: finding.severity })" optionValue="value"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground" title="Needs review?" icon="fa-user-tag">
                            <InputSwitch v-model="finding.needs_review" @change="patchFindingData({ needs_review: finding.needs_review })"></InputSwitch>
                        </InfoCardWithForm>
                    </div>
                </div>

                <div class="grid formgrid p-fluid mt-3">
                    <div class="col-12 field">
                        <label>Proof</label>
                        <MarkdownEditor v-model="finding.proof_text"></MarkdownEditor>
                    </div>
                    <div class="col-12">
                        <FileDrop></FileDrop>
                    </div>
                    <div class="col-12 field">
                        <Button label="Save" @click="patchFindingData({ proof_text: finding.proof_text })"></Button>
                    </div>
                </div>
            </div>
        </div>

        <div :class="containerCol">
            <ProgressBar v-if="!this.previewData && this.showPreview === true" mode="indeterminate" class="h-1rem"></ProgressBar>
            <iframe :src="this.previewUrl" v-if="previewLoading !== true && this.previewData" class="w-full h-full" :key="previewData"></iframe>
        </div>
    </div>
</template>
