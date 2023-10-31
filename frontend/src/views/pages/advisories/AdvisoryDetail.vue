<script>
import AdvisoryService from '@/service/AdvisoryService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import AdvisoryTabMenu from '@/components/pages/AdvisoryTabMenu.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import { useAuthStore } from '@/store/auth';
import ReportTemplateSelectField from '@/components/elements/forms/ReportTemplateSelectField.vue';

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
            templateSelectDialogVisible: false,
            exportTemplate: null,
            downloadPending: false,
            dataLoaded: false,
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
            statusChoices: [
                { title: 'Open', value: 'Open' },
                { title: 'Fixed', value: 'Fixed' },
                { title: "Won't Fix", value: 'Wont Fix' }
            ],
            severityChoices: [
                { label: 'Critical', value: 'Critical' },
                { label: 'High', value: 'High' },
                { label: 'Medium', value: 'Medium' },
                { label: 'Low', value: 'Low' },
                { label: 'Informational', value: 'Informational' }
            ],
            downloadMenuItems: [
                {
                    label: 'Default PDF',
                    command: () => {
                        this.downloadAsPDF();
                    }
                },
                {
                    label: 'Default Markdown',
                    command: () => {
                        this.downloadAsMarkdown();
                    }
                },
                {
                    label: 'PDF with template',
                    command: () => {
                        this.openTemplateSelectDialog();
                    }
                }
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
        closeTemplateSelectDialog() {
            this.templateSelectDialogVisible = false;
        },
        openTemplateSelectDialog() {
            this.templateSelectDialogVisible = true;
        },
        toggleDownloadMenu(event) {
            this.$refs.downloadMenu.toggle(event);
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
        forceFileDownload(response, title) {
            let blob = new Blob([response.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', title);
            link.click();
            this.downloadPending = false;
        },
        forceMarkdownFileDownload(response, title) {
            let blob = new Blob([response.data], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', title);
            link.click();
            this.downloadPending = false;
        },
        downloadAsMarkdown() {
            this.downloadPending = true;
            this.service
                .downloadAdvisoryAsMarkdown(this.$api, this.advisoryId)
                .then((response) => {
                    const filename = 'advisory_' + this.advisoryId + '.md';
                    this.forceMarkdownFileDownload(response, filename);
                })
                .finally(() => {
                    this.downloadPending = false;
                });
        },
        downloadAsPDF() {
            this.downloadPending = true;
            this.closeTemplateSelectDialog();
            let params = {};
            if (this.exportTemplate) {
                params['template'] = this.exportTemplate;
            }
            this.service
                .downloadAdvisoryAsPDF(this.$api, this.advisoryId, params)
                .then((response) => {
                    const filename = 'advisory_' + this.advisoryId + '.pdf';
                    this.forceFileDownload(response, filename);
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
    components: { ReportTemplateSelectField, DetailCardWithIcon, MarkdownEditor, InfoCardWithForm, AdvisoryTabMenu }
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
                <p class="text-xl">{{ advisory.vulnerability.name }} - {{ advisory.internal_name }} ({{ advisory.pk }})</p>
            </div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <Button label="Download" icon="fa fa-download" outlined :loading="downloadPending" :disabled="downloadPending" @click="toggleDownloadMenu"></Button>
                <Menu ref="downloadMenu" :model="downloadMenuItems" :popup="true"></Menu>
                <Button label="Edit" icon="fa fa-pen-to-square" outlined @click="this.$router.push({ name: 'AdvisoryUpdate', params: { advisoryId: this.advisoryId } })"></Button>
                <Button label="Delete" severity="danger" @click="confirmDialogDelete" icon="fa fa-trash" outlined></Button>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <AdvisoryTabMenu class="surface-card"></AdvisoryTabMenu>
            <div class="card" v-if="dataLoaded">
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
                        <DetailCardWithIcon title="CVE-ID" icon="fa fa-barcode" class="surface-ground" :text="advisory.cve_id || '-'"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid">
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Status" icon="fa fa-bookmark">
                            <Dropdown v-model="advisory.status" :options="statusChoices" optionLabel="title" class="w-full" optionValue="value" @change="patchAdvisory({ status: advisory.status })"></Dropdown>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Is Draft?" icon="fa fa-file-pen">
                            <InputSwitch v-model="advisory.is_draft" @change="patchAdvisory({ is_draft: advisory.is_draft })"></InputSwitch>
                        </InfoCardWithForm>
                    </div>
                    <div class="col-12 md:col-3">
                        <InfoCardWithForm class="surface-ground w-full" title="Severity" icon="fa fa-attention">
                            <Dropdown v-model="advisory.severity" :options="severityChoices" optionLabel="label" @change="patchAdvisory({ severity: advisory.severity })" optionValue="value"></Dropdown>
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
    </div>

    <Dialog header="Advisory Export Template" v-model:visible="templateSelectDialogVisible" modal :style="{ width: '70vw' }">
        <div class="grid formgrid p-fluid">
            <div class="field col-12">
                <ReportTemplateSelectField v-model="exportTemplate"></ReportTemplateSelectField>
            </div>
        </div>
        <template #footer>
            <Button label="Cancel" @click="closeTemplateSelectDialog()" class="p-button-outlined"></Button>
            <Button label="Save" @click="this.downloadAsPDF" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>