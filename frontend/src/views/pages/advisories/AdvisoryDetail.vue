<script>
import AdvisoryService, { AdvisoryStatusChoices, VisibilityChoices, VulnerabilityStatusChoices } from '@/service/AdvisoryService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import AdvisoryTabMenu from '@/components/pages/AdvisoryTabMenu.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import { useAuthStore } from '@/store/auth';

export default {
    name: 'AdvisoryDetail',
    mounted() {
        this.getAdvisory();
    },
    data() {
        return {
            service: new AdvisoryService(),
            advisoryId: this.$route.params.advisoryId,
            authStore: useAuthStore(),
            advisory: { vulnerability: {} },
            exportTemplate: null,
            downloadPending: false,
            dataLoaded: false,
            showPreview: false,
            previewData: null,
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.getBreadcrumbRoot()
                },
                {
                    label: 'Advisory Detail',
                    disabled: true
                }
            ],
            vulnerabilityStatusChoices: VulnerabilityStatusChoices,
            statusChoices: AdvisoryStatusChoices,
            visibilityChoices: VisibilityChoices,
            severityChoices: [
                { label: 'Critical', value: 'Critical' },
                { label: 'High', value: 'High' },
                { label: 'Medium', value: 'Medium' },
                { label: 'Low', value: 'Low' },
                { label: 'Informational', value: 'Informational' }
            ]
        };
    },
    methods: {
        getBreadcrumbRoot() {
            if (this.$router.options.history.state.back === '/advisories/inbox') {
                return this.$router.resolve({
                    name: 'AdvisoryInbox'
                });
            }
            return this.$router.resolve({
                name: 'AdvisoryList'
            });
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
            let config = {
                responseType: 'arraybuffer'
            };
            this.$api.get('/advisories/' + this.advisoryId + '/preview/', config).then((response) => {
                this.previewData = response.data;
            });
        },
        getAdvisory() {
            this.service.getAdvisory(this.$api, this.advisoryId).then((response) => {
                this.advisory = response.data;
                if (this.advisory.recommendation === null) {
                    this.advisory.recommendation = '';
                }
                if (this.advisory.description === null) {
                    this.advisory.description = '';
                }
                this.dataLoaded = true;
            });
        },
        patchAdvisory(data) {
            this.service.patchAdvisory(this.$api, this.advisoryId, data).then((response) => {
                this.advisory = response.data;
                if (this.showPreview === true) {
                    this.getPreviewData();
                }
                this.$toast.add({
                    severity: 'success',
                    summary: 'Advisory updated!',
                    life: 3000,
                    detail: 'Advisory was updated!'
                });
            });
        },
        patchAdvisoryDisclosureDate() {
            let data = {
                date_planned_disclosure: this.advisory.date_planned_disclosure.toISOString().split('T')[0]
            };
            this.patchAdvisory(data);
        },
        patchAdvisoryDescription() {
            let data = {
                description: this.advisory.description
            };
            this.patchAdvisory(data);
        },
        patchRecommendation() {
            let data = {
                recommendation: this.advisory.recommendation
            };
            this.patchAdvisory(data);
        },
        forceFileDownload(response) {
            let blob = new Blob([response.data], { type: response.headers['Content-Type'] });
            let filename = response.headers['content-disposition'].split('filename=')[1].split(';')[0];
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            link.click();
            this.downloadPending = false;
        },
        downloadAsPDF() {
            this.downloadPending = true;
            let params = {};
            if (this.exportTemplate) {
                params['template'] = this.exportTemplate;
            }
            this.service
                .downloadAdvisoryAsPDF(this.$api, this.advisoryId, params)
                .then((response) => {
                    this.forceFileDownload(response);
                    this.exportTemplate = null;
                })
                .finally(() => {
                    this.downloadPending = false;
                });
        },
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this advisory?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteAdvisory(this.$api, this.advisoryId).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Confirmed',
                            detail: 'Advisory deleted!',
                            life: 3000
                        });
                        this.$router.push({
                            name: 'AdvisoryList'
                        });
                    });
                }
            });
        }
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
        }
    },
    components: { DetailCardWithIcon, MarkdownEditor, InfoCardWithForm, AdvisoryTabMenu }
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
                <p class="text-xl">
                    {{ advisory.vulnerability.name }} - {{ advisory.internal_name }} ({{ advisory.pk }}) <span v-if="advisory.cve_id">/ {{ advisory.cve_id }}</span>
                </p>
            </div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <Button icon="fa fa-eye" outlined label="Preview" @click="togglePreview"></Button>

                <Button label="Download" icon="fa fa-download" outlined :loading="downloadPending" :disabled="downloadPending" @click="downloadAsPDF"></Button>
                <Button label="Edit" icon="fa fa-pen-to-square" outlined @click="this.$router.push({ name: 'AdvisoryUpdate', params: { advisoryId: this.advisoryId } })"></Button>
                <Button label="Delete" severity="danger" @click="confirmDialogDelete" icon="fa fa-trash" outlined></Button>
            </div>
        </div>
    </div>

    <div class="grid">
        <div :class="containerCol">
            <AdvisoryTabMenu class="surface-card"></AdvisoryTabMenu>
            <div class="card border-noround-top" v-if="dataLoaded">
                <div class="grid">
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Product" icon="fa fa-cart-shopping" class="surface-ground" :text="advisory.product + '(by ' + advisory.vendor_name + ')'"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Affected Versions" icon="fa fa-circle-exclamation" class="surface-ground" :text="advisory.affected_versions"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Fixed Versions" icon="fa fa-screwdriver-wrench" class="surface-ground" :text="advisory.fixed_version || '-'"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Visibility" icon="fa fa-file-pen">
                            <Dropdown v-model="advisory.visibility" :options="visibilityChoices" optionLabel="label" optionValue="value" @change="patchAdvisory({ visibility: advisory.visibility })"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                </div>
                <div class="grid">
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Severity" icon="fa fa-shield-halved">
                            <Dropdown v-model="advisory.severity" :options="severityChoices" optionLabel="label" @change="patchAdvisory({ severity: advisory.severity })" optionValue="value"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Vulnerability Status" icon="fa fa-file-pen">
                            <Dropdown v-model="advisory.vulnerability_status" :options="vulnerabilityStatusChoices" optionLabel="label" optionValue="value" @change="patchAdvisory({ vulnerability_status: advisory.vulnerability_status })"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Status" icon="fa fa-bookmark">
                            <Dropdown v-model="advisory.status" :options="statusChoices" optionLabel="label" optionValue="value" @change="patchAdvisory({ status: advisory.status })"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground" title="Planned Disclosure" icon="fa-calendar">
                            <Calendar v-model="advisory.date_planned_disclosure" @update:modelValue="patchAdvisoryDisclosureDate"></Calendar>
                        </InfoCardWithForm>
                    </div>
                </div>
                <div class="grid formgrid p-fluid">
                    <div class="field col-12">
                        <label>Description</label>
                        <MarkdownEditor v-model="advisory.description" @blur="patchAdvisoryDescription"></MarkdownEditor>
                    </div>
                    <div class="col-12 field">
                        <label>Recommendation</label>
                        <MarkdownEditor v-model="advisory.recommendation" @blur="patchRecommendation"></MarkdownEditor>
                    </div>
                </div>
            </div>

            <div class="card" v-else>
                <Skeleton class="mb-2"></Skeleton>
                <Skeleton width="10rem" class="mb-2"></Skeleton>
                <Skeleton width="5rem" class="mb-2"></Skeleton>
                <Skeleton height="2rem" class="mb-2"></Skeleton>
                <Skeleton width="10rem" height="4rem"></Skeleton>
            </div>
        </div>

        <div :class="containerCol" v-if="showPreview === true">
            <ProgressBar v-if="!this.previewData && this.showPreview === true" mode="indeterminate" class="h-1rem"></ProgressBar>
            <iframe :src="previewUrl" v-if="this.previewData" :key="this.previewData" class="w-full h-full"></iframe>
        </div>
    </div>
</template>
