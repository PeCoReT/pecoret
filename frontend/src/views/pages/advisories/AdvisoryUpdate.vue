<script>
import SeveritySelectField from '@/components/forms/fields/SeveritySelectField.vue';
import { useAuthStore } from '@/store/auth';
import AdvisoryLabelSelectField from '@/components/forms/fields/advisories/AdvisoryLabelSelectField.vue';
import ReportTemplateSelectField from '@/components/forms/fields/ReportTemplateSelectField.vue';
import TechnologySelectField from '@/components/forms/fields/TechnologySelectField.vue';

export default {
    name: 'AdvisoryUpdate',
    data() {
        return {
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
                title: this.model.title,
                technology: this.model.technology,
                affected_versions: this.model.affected_versions,
                fixed_version: this.model.fixed_version,
                hide_advisory_id_in_report: this.model.hide_advisory_id_in_report,
                custom_report_title: this.model.custom_report_title,
                cve_id: this.model.cve_id,
                researchers: this.model.researchers,
                vulnerability_id: this.model.template,
                report_template: this.model.report_template,
                labels: []
            };
            if (this.model.technology && this.model.technology.pk) {
                data['technology'] = this.model.technology.pk;
            }

            this.model.labels.forEach((item) => {
                if (item.pk) {
                    item = item.pk;
                }
                data['labels'].push(item);
            });
            this.$api
                .patch(this.$api.e.advisoryDetail, { pk: this.advisoryId }, data)
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
            this.$api.get(this.$api.e.vulnTemplateList).then((response) => {
                this.templateChoices = response.data.results;
            });
        },
        onFilterTemplate(event) {
            let params = {
                search: event.value
            };
            this.$api.get(this.$api.e.vulnTemplateList, null, params).then((response) => {
                this.templateChoices = response.data.results;
            });
        },
        getAdvisory() {
            this.$api.get(this.$api.e.advisoryDetail, { pk: this.advisoryId }).then((response) => {
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
    components: { TechnologySelectField, ReportTemplateSelectField, SeveritySelectField, AdvisoryLabelSelectField }
};
</script>
<template>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <div class="card">
                <Form v-if="loaded">
                    <InlineFieldGroup>
                        <InlineField label="Vulnerability Template">
                            <Select :options="templateChoices" optionLabel="name" optionValue="vulnerability_id" @focus="onFocusTemplate" filter @filter="onFilterTemplate" v-model="model.template"></Select>
                        </InlineField>
                        <InlineField label="Title">
                            <InputText id="name" v-model="model.title"></InputText>
                        </InlineField>
                    </InlineFieldGroup>
                    <Field label="Product">
                        <TechnologySelectField v-model="model.technology"></TechnologySelectField>
                    </Field>
                    <InlineFieldGroup>
                        <InlineField label="Affected Versions">
                            <InputText id="affected_versions" v-model="model.affected_versions"></InputText>
                        </InlineField>
                        <InlineField label="Fixed Version">
                            <InputText id="fixed_versions" v-model="model.fixed_version"></InputText>
                        </InlineField>
                    </InlineFieldGroup>
                    <Field label="Labels">
                        <AdvisoryLabelSelectField v-model="model.labels"></AdvisoryLabelSelectField>
                    </Field>
                    <InlineFieldGroup>
                        <InlineField label="Report Template">
                            <ReportTemplateSelectField v-model="model.report_template"></ReportTemplateSelectField>
                        </InlineField>
                        <InlineField label="Custom Report Title">
                            <InputText id="custom_title" v-model="model.custom_report_title"></InputText>
                        </InlineField>
                    </InlineFieldGroup>
                    <InlineFieldGroup>
                        <InlineField label="Researchers">
                            <InputText id="researchers" v-model="model.researchers"></InputText>
                            <small id="researchers-help">Overwrites the researchers section in the report (default: your display name).</small>
                        </InlineField>
                        <InlineField label="CVE-ID">
                            <InputText id="cve-id" v-model="model.cve_id"></InputText>
                        </InlineField>
                    </InlineFieldGroup>
                    <Field>
                        <div class="flex flex-row">
                            <ToggleSwitch v-model="model.hide_advisory_id_in_report"></ToggleSwitch>
                            <label class="ml-3">Hide advisory id in report?</label>
                        </div>
                    </Field>
                    <Button label="Save" :loading="loading" @click="update" class="w-full"></Button>
                </Form>

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
