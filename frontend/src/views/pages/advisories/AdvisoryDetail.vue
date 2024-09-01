<script>
import AdvisoryService, { AdvisoryStatusChoices, VulnerabilityStatusChoices } from '@/service/AdvisoryService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import AdvisoryTabMenu from '@/components/navigation/AdvisoryTabMenu.vue';
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
            advisory: { vulnerability: {}, technology: {}, user: {} },
            exportTemplate: null,
            downloadPending: false,
            dataLoaded: false,
            showPreview: false,
            previewData: null,
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({ name: 'AdvisoryList' })
                },
                {
                    label: 'Advisory Detail',
                    disabled: true
                }
            ],
            vulnerabilityStatusChoices: VulnerabilityStatusChoices,
            statusChoices: AdvisoryStatusChoices,
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
            this.service.getAdvisory(this.advisoryId).then((response) => {
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
            this.service.patchAdvisory(this.advisoryId, data).then((response) => {
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
                .downloadAdvisoryAsPDF(this.advisoryId, params)
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
                    this.service.deleteAdvisory(this.advisoryId).then(() => {
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
        productDisplay() {
            if (this.advisory.technology && this.advisory.technology.vendor) {
                return `${this.advisory.technology.name} (by ${this.advisory.technology.vendor})`;
            }
            return `${this.advisory.technology.name} (by Unknown)`;
        },
        containerCol() {
            if (this.showPreview === true) {
                return 'col-span-6';
            }
            return 'col-span-12';
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
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-6">
            <div class="flex justify-start">
                <p class="text-xl">
                    {{ advisory.vulnerability.name }} - {{ advisory.title }} ({{ advisory.advisory_id }}) <span v-if="advisory.cve_id">/ {{ advisory.cve_id }}</span>
                </p>
            </div>
        </div>
        <div class="col-span-6">
            <div class="flex justify-end">
                <Button icon="fa fa-eye" outlined label="Preview" @click="togglePreview"></Button>

                <Button label="Download" icon="fa fa-download" outlined :loading="downloadPending" :disabled="downloadPending" @click="downloadAsPDF"></Button>
                <Button label="Edit" icon="fa fa-pen-to-square" outlined @click="this.$router.push({ name: 'AdvisoryUpdate', params: { advisoryId: this.advisoryId } })"></Button>
                <Button label="Delete" severity="danger" @click="confirmDialogDelete" icon="fa fa-trash" outlined></Button>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-12 gap-3 mt-3">
        <div :class="containerCol">
            <AdvisoryTabMenu></AdvisoryTabMenu>
            <div class="card border-noround-top" v-if="dataLoaded">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Product" icon="fa fa-cart-shopping" class="bg-surface-950" :text="productDisplay"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Affected Versions" icon="fa fa-circle-exclamation" class="bg-surface-950" :text="advisory.affected_versions"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Fixed Versions" icon="fa fa-screwdriver-wrench" class="bg-surface-950" :text="advisory.fixed_version || '-'"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="User" icon="fa fa-user" class="bg-surface-950" :text="advisory.user.username"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid grid-cols-12 mt-3 gap-3">
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950 w-full" title="Severity" icon="fa fa-shield-halved">
                            <Select v-model="advisory.severity" :options="severityChoices" optionLabel="label" @change="patchAdvisory({ severity: advisory.severity })" optionValue="value"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950 w-full" title="Vulnerability Status" icon="fa fa-file-pen">
                            <Select v-model="advisory.vulnerability_status" :options="vulnerabilityStatusChoices" optionLabel="label" optionValue="value" @change="patchAdvisory({ vulnerability_status: advisory.vulnerability_status })"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950 w-full" title="Status" icon="fa fa-bookmark">
                            <Select v-model="advisory.status" :options="statusChoices" optionLabel="label" optionValue="value" @change="patchAdvisory({ status: advisory.status })"></Select>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <InfoCardWithForm class="bg-surface-950" title="Planned Disclosure" icon="fa-calendar">
                            <DatePicker v-model="advisory.date_planned_disclosure" @update:modelValue="patchAdvisoryDisclosureDate"></DatePicker>
                        </InfoCardWithForm>
                    </div>
                </div>
                <div class="grid grid-cols-12 mt-3">
                    <div class="col-span-12">
                        <Form>
                            <Field label="Description">
                                <MarkdownEditor v-model="advisory.description" @blur="patchAdvisoryDescription"></MarkdownEditor>
                            </Field>
                            <Field label="Recommendation">
                                <MarkdownEditor v-model="advisory.recommendation" @blur="patchRecommendation"></MarkdownEditor>
                            </Field>
                        </Form>
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
