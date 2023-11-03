<script>
import AdvisoryService from '@/service/AdvisoryService';
import VulnerabilityTemplateService from '@/service/VulnerabilityTemplateService';
import SeveritySelectField from '@/components/elements/forms/SeveritySelectField.vue';
import { useAuthStore } from '@/store/auth';
import AdvisoryLabelSelectField from '@/components/elements/forms/AdvisoryLabelSelectField.vue';
import ReportTemplateSelectField from "@/components/elements/forms/ReportTemplateSelectField.vue";

export default {
    name: 'AdvisoryUpdate',
    data() {
        return {
            service: new AdvisoryService(),
            templateService: new VulnerabilityTemplateService(),
            advisoryId: this.$route.params.advisoryId,
            authStore: useAuthStore(),
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Advisory Detail',
                    to: this.$router.resolve({
                        name: 'AdvisoryDetail',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Update',
                    disabled: true
                }
            ],
            model: {},
            templateChoices: [],
            loading: false,
            loaded: false
        };
    },
    methods: {
        update() {
            this.loading = true;
            let data = {
                internal_name: this.model.internal_name,
                product: this.model.product,
                affected_versions: this.model.affected_versions,
                fixed_version: this.model.fixed_version,
                vendor_name: this.model.vendor_name,
                vendor_url: this.model.vendor_url,
                hide_advisory_id_in_report: this.model.hide_advisory_id_in_report,
                custom_report_title: this.model.custom_report_title,
                cve_id: this.model.cve_id,
                vulnerability_id: this.model.template,
                report_template: this.model.report_template
            };
            if (this.authStore.groups.isAdvisoryManagement === true) {
                data['labels'] = [];
                this.model.labels.forEach((item) => {
                    if (item.pk) {
                        item = item.pk;
                    }
                    data['labels'].push(item);
                });
            }
            this.service
                .patchAdvisory(this.$api, this.advisoryId, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Advisory created!',
                        life: 3000,
                        detail: 'Advisory was created successfully!'
                    });
                    this.$router.push({
                        name: 'AdvisoryDetail',
                        params: {
                            advisoryId: response.data.pk
                        }
                    });
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onFocusTemplate() {
            this.templateService.getTemplates(this.$api).then((response) => {
                this.templateChoices = response.data.results;
            });
        },
        onFilterTemplate(event) {
            let params = {
                search: event.value
            };
            this.templateService.getTemplates(this.$api, params).then((response) => {
                this.templateChoices = response.data.results;
            });
        },
        getAdvisory() {
            this.service.getAdvisory(this.$api, this.advisoryId).then((response) => {
                this.model = response.data;
                this.model.template = response.data.vulnerability.vulnerability_id;
                this.templateChoices.push(response.data.vulnerability);
                this.loaded = true;
            });
        }
    },
    mounted() {
        this.getAdvisory();
    },
    components: { ReportTemplateSelectField, SeveritySelectField, AdvisoryLabelSelectField }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="p-fluid formgrid grid" v-if="loaded">
                    <div class="field col-12">
                        <label for="template">Vulnerability Template</label>
                        <Dropdown :options="templateChoices" optionLabel="name" optionValue="vulnerability_id" @focus="onFocusTemplate" filter @filter="onFilterTemplate" v-model="model.template"></Dropdown>
                    </div>
                    <div class="field col-12">
                        <label for="name">Internal Name</label>
                        <InputText id="name" v-model="model.internal_name"></InputText>
                    </div>
                    <div class="field col-12">
                        <SeveritySelectField v-model="model.severity"></SeveritySelectField>
                    </div>
                    <div class="field col-12">
                        <label for="product">Product</label>
                        <InputText id="product" v-model="model.product"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="affected_versions">Affected Versions</label>
                        <InputText id="affected_versions" v-model="model.affected_versions"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="fixed_versions">Fixed Version</label>
                        <InputText id="fixed_versions" v-model="model.fixed_version"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="vendor_name">Vendor</label>
                        <InputText id="vendor_name" v-model="model.vendor_name"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="vendor_url">Vendor URL</label>
                        <InputText id="vendor_url" v-model="model.vendor_url"></InputText>
                    </div>
                    <div class="field col-12" v-if="authStore.groups.isAdvisoryManagement === true">
                        <AdvisoryLabelSelectField v-model="model.labels"></AdvisoryLabelSelectField>
                    </div>
                    <div class="field col-12">
                        <ReportTemplateSelectField v-model="model.report_template"></ReportTemplateSelectField>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="custom_title">Custom Report Title</label>
                        <InputText id="custom_title" v-model="model.custom_report_title"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="cve-id">CVE-ID</label>
                        <InputText id="cve-id" v-model="model.cve_id"></InputText>
                    </div>
                    <div class="field col-12">
                        <InputSwitch v-model="model.hide_advisory_id_in_report" id="hide_id"></InputSwitch>
                        <label for="hide_id" class="ml-3">Hide advisory id in report?</label>
                    </div>
                    <div class="mt-3 col-12">
                        <div class="justify-content-end flex">
                            <Button label="Save" :loading="loading" @click="update"></Button>
                        </div>
                    </div>
                </div>

                <div v-else class="grid w-full">
                    <Skeleton class="mb-2"></Skeleton>
                    <Skeleton width="10rem" class="mb-2"></Skeleton>
                    <Skeleton width="5rem" class="mb-2"></Skeleton>
                    <Skeleton height="2rem" class="mb-2"></Skeleton>
                    <Skeleton width="10rem" height="4rem"></Skeleton>
                </div>
            </div>
        </div>
    </div>
</template>