<script>
import { projectVisibilityChoices } from '@/utils/constants';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ModelCombobox } from '@/components/combobox';
import { DatePicker } from '@/components/datepicker';
import { Select } from '@/components/select';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { PageHeader } from '@/components/typography';

export default {
    name: 'ProjectCreate',
    components: {
        ContainerLayout,
        MultiModelCombobox,
        Textarea,
        ModelCombobox,
        Input,
        Button,
        DatePicker,
        Select,
        PageHeader
    },
    data() {
        return {
            model: {
                project_types: [],
                name: null,
                start_date: null,
                end_date: null,
                test_method: null,
                language: null,
                description: '',
                require_cvss_score: null,
                company: null,
                visibility: null
            },
            scoreChoices: [
                { label: 'CVSS 4.0 Base', value: '0' },
                { label: 'CVSS 3.1 Base', value: '1' }
            ],
            testMethodChoices: [
                { label: 'Unknown', value: 'Unknown' },
                { label: 'Greybox', value: 'Grey Box' },
                { label: 'Blackbox', value: 'Black Box' },
                { label: 'Whitebox', value: 'White Box' }
            ],
            companyChoices: null,
            languageChoices: null
        };
    },
    methods: {
        projectVisibilityChoices() {
            return projectVisibilityChoices;
        },
        create() {
            this.loading = true;
            let data = {
                project_types: this.model.project_types,
                name: this.model.name,
                start_date: this.model.start_date,
                end_date: this.model.end_date,
                status: 'Open',
                test_method: this.model.test_method,
                language: this.model.language,
                require_cvss_base_score: this.model.require_cvss_base_score,
                description: this.model.description,
                company: this.model.company,
                visibility: this.model.visibility
            };
            this.$api
                .post(this.$api.e.projectList, null, data)
                .then((response) => {
                    this.$toaster({
                        title: 'Created',
                        duration: 3000,
                        description: 'Project created successfully!'
                    });
                    this.$router.push({ name: 'ProjectDetail', params: { projectId: response.data.pk } });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <PageHeader>Create Project</PageHeader>
        <Form>
            <Field label="Name">
                <Input v-model="model.name"></Input>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Start Date">
                    <DatePicker v-model="model.start_date"></DatePicker>
                </InlineField>
                <InlineField label="End Date">
                    <DatePicker v-model="model.end_date"></DatePicker>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Test Method">
                <Select v-model="model.test_method" :options="testMethodChoices"></Select>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Project Types">
                    <MultiModelCombobox v-model="model.project_types" :options-url="this.$api.e.pentestTypeList" align="start" class="w-full" title=""></MultiModelCombobox>
                </InlineField>
                <InlineField label="Language">
                    <ModelCombobox v-model="model.language" :api-endpoint="this.$api.e.projectsAvailableLanguages" align="start" label-field="language" value-field="language" variant="form"></ModelCombobox>
                </InlineField>
            </InlineFieldGroup>
            <InlineFieldGroup>
                <InlineField label="Company">
                    <ModelCombobox v-model="model.company" :api-endpoint="this.$api.e.companyList" align="start" label-field="name" value-field="pk" variant="form"> </ModelCombobox>
                </InlineField>
                <InlineField label="Visibility">
                    <Select v-model="model.visibility" :options="projectVisibilityChoices()"></Select>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Require CVSS Score">
                <Select v-model="model.require_cvss_score" :options="scoreChoices" :show-clear="true"></Select>
            </Field>
            <Field label="Description">
                <Textarea v-model="model.description" autoResize cols="30" rows="5"></Textarea>
            </Field>
            <Button class="w-full" @click="create">Save</Button>
        </Form>
    </ContainerLayout>
</template>
