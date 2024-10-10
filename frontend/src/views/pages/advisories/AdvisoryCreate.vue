<script>
import AdvisoryService from '@/service/AdvisoryService';
import VulnerabilityTemplateService from '@/service/VulnerabilityTemplateService';
import SeveritySelectField from '@/components/forms/fields/SeveritySelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologySelectField from '@/components/forms/fields/TechnologySelectField.vue';
import BaseLayout from '@/layout/base/BaseLayout.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';
import InlineField from '@/components/common/forms/InlineField.vue';
import AlertPanel from '@/components/panels/Alert.vue';
import { warn } from 'vue';

export default {
    name: 'AdvisoryCreate',
    data() {
        return {
            service: new AdvisoryService(),
            templateService: new VulnerabilityTemplateService(),
            advisoryId: null,
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Create',
                    disabled: true
                }
            ],
            activeStep: 0,
            stepItems: [
                {
                    label: 'Vendor & Description'
                },
                {
                    label: 'Proof of Concept'
                },
                {
                    label: 'Recommendation'
                }
            ],
            model: {
                title: null,
                template: null,
                product: null,
                affected_versions: null,
                fixed_version: null,
                severity: null,
                technology: null,
                researchers: null
            },
            descriptionCustomized: false,
            loading: false,
            templateChoices: []
        };
    },
    methods: {
        warn,
        async create() {
            this.loading = true;
            let data = {
                title: this.model.title,
                vulnerability_id: this.model.template,
                product: this.model.product,
                description: this.model.description,
                affected_versions: this.model.affected_versions,
                fixed_version: this.model.fixed_version,
                severity: this.model.severity,
                technology: this.model.technology,
                researchers: this.model.researchers,
                proof_text: this.model.proof_text,
                report_template: 'default_template'
            };
            this.service
                .createAdvisory(data)
                .then((response) => {
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

            this.loading = false;
        },
        preSelectTemplateValues() {
            this.templateChoices.forEach((item) => {
                if (item.vulnerability_id === this.model.template) {
                    this.model.severity = item.severity;
                    this.model.recommendation = item.recommendation;
                }
            });
        },
        setDescription(item) {
            // set a default description based on the technology description
            if (this.descriptionCustomized === false || (this.descriptionCustomized === true && this.description === '')) {
                this.model.description = item.description;
            }
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
        }
    },
    mounted() {},
    components: {
        AlertPanel,
        InlineField,
        InlineFieldGroup,
        BaseLayout,
        TechnologySelectField,
        SeveritySelectField,
        MarkdownEditor
    }
};
</script>
<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <div class="col-span-12 card">
            <Steps v-model:activeStep="activeStep" :model="stepItems" class="mb-3"></Steps>
            <Form v-if="activeStep === 0">
                <Field label="Title">
                    <InputText id="name" v-model="model.title"></InputText>
                </Field>
                <InlineFieldGroup>
                    <InlineField label="Vulnerability Template">
                        <Select :options="templateChoices" optionLabel="name" optionValue="vulnerability_id" @change="preSelectTemplateValues" @focus="onFocusTemplate" filter @filter="onFilterTemplate" v-model="model.template"></Select>
                    </InlineField>
                    <InlineField label="Severity">
                        <SeveritySelectField v-model="model.severity"></SeveritySelectField>
                    </InlineField>
                </InlineFieldGroup>
                <InlineFieldGroup>
                    <InlineField label="Product">
                        <TechnologySelectField v-model="model.technology" @change="setDescription"></TechnologySelectField>
                    </InlineField>
                    <InlineField label="Affected Versions">
                        <InputText id="affected_versions" v-model="model.affected_versions"></InputText>
                    </InlineField>
                </InlineFieldGroup>
                <Field label="Researchers">
                    <InputText id="researchers" v-model="model.researchers"></InputText>
                    <small id="researchers-help">Overwrites the researchers section in the report (default: your display name).</small>
                </Field>
                <Field label="Description">
                    <MarkdownEditor v-model="model.description"></MarkdownEditor>
                </Field>
                <Button label="Next" @click="activeStep = 1" class="w-full"></Button>
            </Form>
            <Form v-else-if="activeStep === 1">
                <AlertPanel message="Images can only be uploaded after advisory was created!" type="warning"></AlertPanel>
                <Field label="Proof">
                    <MarkdownEditor v-model="model.proof_text"></MarkdownEditor>
                </Field>
                <div class="flex gap-6">
                    <Button label="Back" @click="activeStep = 0" outlined class="w-1/2"></Button>

                    <Button label="Next" @click="activeStep = 2" class="w-1/2"></Button>
                </div>
            </Form>
            <Form v-else-if="activeStep === 2">
                <Field label="Recommendation">
                    <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
                </Field>
                <div class="flex gap-6">
                    <Button label="Back" @click="activeStep = 1" outlined :disabled="loading" class="w-1/2"></Button>
                    <Button label="Save" :loading="loading" @click="create" class="w-1/2"></Button>
                </div>
            </Form>
        </div>
    </BaseLayout>
</template>
