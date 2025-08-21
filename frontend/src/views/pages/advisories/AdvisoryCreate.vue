<script>
import { SeveritySelectField, TechnologySelectField } from '@/partials/common';
import { MarkdownEditor } from '@/components/editor';
import { Alert } from '@/components/alert';
import { warn } from 'vue';
import { Stepper, StepperDescription, StepperIndicator, StepperItem, StepperSeparator, StepperTitle, StepperTrigger } from '@/components/ui/stepper';
import { Input } from '@/components/ui/input';
import { ModelCombobox } from '@/components/combobox';
import { Button } from '@/components/ui/button';
import { Select } from '@/components/select';
import { severityChoices } from '@/utils/constants';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { PageHeader } from '@/components/typography';

export default {
    name: 'AdvisoryCreate',
    data() {
        return {
            advisoryId: null,
            activeStep: 1,
            stepItems: [
                {
                    step: 1,
                    label: 'Vendor & Description',
                    icon: 'fa fa-pen'
                },
                {
                    step: 2,
                    label: 'Proof of Concept',
                    icon: 'fa fa-receipt'
                },
                {
                    step: 3,
                    label: 'Recommendation',
                    icon: 'fa fa-user-doctor'
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
                researchers: null,
                report_template: null,
                cvss_vector: null,
                cwes: []
            },
            descriptionCustomized: false,
            loading: false
        };
    },
    methods: {
        severityChoices() {
            return severityChoices;
        },
        warn,
        async create() {
            this.loading = true;
            let data = {
                title: this.model.title,
                product: this.model.product,
                description: this.model.description,
                affected_versions: this.model.affected_versions,
                fixed_version: this.model.fixed_version,
                severity: this.model.severity,
                technology: this.model.technology,
                researchers: this.model.researchers,
                proof_text: this.model.proof_text,
                report_template: this.model.report_template,
                cvss_vector: this.model.cvss_vector,
                cwes: this.model.cwes,
                recommendation: this.model.recommendation
            };
            this.$api
                .post(this.$api.e.advisoryList, null, data)
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
        }
    },
    mounted() {},
    components: {
        ModelCombobox,
        MultiModelCombobox,
        Alert,
        TechnologySelectField,
        SeveritySelectField,
        MarkdownEditor,
        Stepper,
        StepperDescription,
        StepperIndicator,
        StepperItem,
        StepperSeparator,
        StepperTitle,
        StepperTrigger,
        Input,
        Select,
        Button,
        ContainerLayout,
        PageHeader
    }
};
</script>
<template>
    <ContainerLayout>
        <template #pre-content>
            <PageHeader>New Advisory</PageHeader>
        </template>
        <div class="col-span-12">
            <Stepper class="flex w-full items-start gap-2 mb-3" v-model="activeStep">
                <StepperItem v-for="item in stepItems" :key="item.step" :step="item.step" class="relative flex w-full flex-col items-center justify-center">
                    <StepperTrigger>
                        <StepperIndicator>
                            <i class="w-4 h-4" :class="item.icon"></i>
                        </StepperIndicator>
                        <div class="flex flex-col">
                            <StepperTitle>{{ item.label }}</StepperTitle>
                        </div>
                    </StepperTrigger>
                    <StepperSeparator
                        v-if="item.step !== stepItems[stepItems.length - 1].step"
                        class="absolute left-[calc(50%+20px)] right-[calc(-50%+10px)] top-5 block h-0.5 shrink-0 rounded-full bg-muted group-data-[state=completed]:bg-primary"
                    ></StepperSeparator>
                </StepperItem>
            </Stepper>
            <Form v-if="activeStep === 1">
                <Field label="Title">
                    <Input id="name" v-model="model.title"></Input>
                </Field>
                <InlineFieldGroup>
                    <InlineField label="CWEs">
                        <MultiModelCombobox variant="form" value-field="pk" label-field="name" v-model="model.cwes" title="" :options-url="this.$api.e.cweList"></MultiModelCombobox>
                    </InlineField>
                    <InlineField label="Severity">
                        <Select :options="severityChoices()" v-model="model.severity"></Select>
                    </InlineField>
                </InlineFieldGroup>
                <InlineFieldGroup>
                    <InlineField label="Product">
                        <ModelCombobox variant="form" v-model="model.technology" label="" :api-endpoint="this.$api.e.technologyList"></ModelCombobox>
                    </InlineField>
                    <InlineField label="Affected Versions">
                        <Input id="affected_versions" v-model="model.affected_versions"></Input>
                    </InlineField>
                </InlineFieldGroup>
                <Field label="CVSS">
                    <Input id="cvss" v-model="model.cvss_vector"></Input>
                </Field>
                <InlineFieldGroup>
                    <InlineField label="Researchers">
                        <Input id="researchers" v-model="model.researchers"></Input>
                        <small id="researchers-help">Overwrites the researchers section in the report (default: your display name).</small>
                    </InlineField>
                    <InlineField label="Report Template">
                        <ModelCombobox v-model="model.report_template" :api-endpoint="this.$api.e.reportTemplateList" align="start" label="" value-field="name" variant="form"></ModelCombobox>
                    </InlineField>
                </InlineFieldGroup>

                <Field label="Description">
                    <MarkdownEditor v-model="model.description"></MarkdownEditor>
                </Field>
                <Button class="w-full" @click="activeStep = 2">Next</Button>
            </Form>
            <Form v-else-if="activeStep === 2">
                <Alert message="Images can only be uploaded after advisory was created!" type="warning"></Alert>
                <Field label="Proof">
                    <MarkdownEditor v-model="model.proof_text"></MarkdownEditor>
                </Field>
                <div class="flex gap-6">
                    <Button class="w-1/2" @click="activeStep = 1" variant="outline">Back</Button>

                    <Button class="w-1/2" @click="activeStep = 3">Next</Button>
                </div>
            </Form>
            <Form v-else-if="activeStep === 3">
                <Field label="Recommendation">
                    <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
                </Field>
                <div class="flex gap-6">
                    <Button :disabled="loading" class="w-1/2" @click="activeStep = 2" variant="outline">Back</Button>
                    <Button :loading="loading" class="w-1/2" @click="create">Save</Button>
                </div>
            </Form>
        </div>
    </ContainerLayout>
</template>
