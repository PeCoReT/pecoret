<script>
import { useAuthStore } from '@/store/auth';
import { projectVisibilityChoices } from '@/utils/constants';
import { CompanySelectField } from '@/partials/companies';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { Select } from '@/components/select';
import { Input } from '@/components/ui/input';
import { DatePicker } from '@/components/datepicker';
import { Button } from '@/components/ui/button';
import { ModelCombobox, MultiModelCombobox } from '@/components/combobox';
import { Textarea } from '@/components/ui/textarea';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import {PageHeader} from "@/components/typography";

export default {
    name: 'ProjectUpdate',
    components: {
        ContainerLayout,
        MultiModelCombobox,
        ModelCombobox,
        Button,
        DefaultSkeleton,
        CompanySelectField,
        Select,
        Input,
        DatePicker,
        Textarea,
        PageHeader
    },
    data() {
        return {
            loading: false,
            authStore: useAuthStore(),
            model: null,
            projectId: this.$route.params.projectId,
            availableLanguages: [],
            companyChoices: null,
            testMethodChoices: [
                { label: 'Unknown', value: 'Unknown' },
                { label: 'Greybox', value: 'Grey Box' },
                { label: 'Blackbox', value: 'Black Box' },
                { label: 'Whitebox', value: 'White Box' }
            ],
            scoreChoices: [
                { label: 'CVSS 4.0 Base', value: 0 },
                { label: 'CVSS 3.1 Base', value: 1 }
            ]
        };
    },
    mounted() {
        this.$api.get(this.$api.e.projectDetail, { pk: this.projectId }).then((response) => {
            this.model = response.data;
        });
        this.getLanguages();
    },
    methods: {
        projectVisibilityChoices() {
            return projectVisibilityChoices;
        },
        getLanguages() {
            this.$api.get(this.$api.e.projectsAvailableLanguages).then((response) => {
                this.availableLanguages = response.data;
            });
        },
        save() {
            this.loading = true;
            if (typeof this.model.project_types === 'object') {
                if (this.model.project_types.length > 0) {
                    if (this.model.project_types[0].pk) {
                        delete this.model.project_types;
                    }
                }
            }
            let data = {
                project_types: this.model.project_types,
                name: this.model.name,
                start_date: this.model.start_date,
                end_date: this.model.end_date,
                test_method: this.model.test_method,
                language: this.model.language,
                require_cvss_score: this.model.require_cvss_score,
                description: this.model.description,
                company: this.model.company,
                visibility: this.model.visibility
            };
            if (this.authStore.groups.isManagement !== true) {
                delete data['visibility'];
            }
            if (this.model.company && this.model.company.pk) {
                data['company'] = this.model.company.pk;
            }
            this.$api
                .patch(this.$api.e.projectDetail, { pk: this.projectId }, data)
                .then(() => {
                    this.authStore.activateProject(this.model);
                    this.$router.push({ name: 'ProjectDetail', params: { projectId: this.projectId } });
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
        <PageHeader>Update Project</PageHeader>
        <Form v-if="model">
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
                    <MultiModelCombobox v-model="model.project_types" :options-url="this.$api.e.pentestTypeList" title="Project Types"></MultiModelCombobox>
                </InlineField>
                <InlineField label="Language">
                    <ModelCombobox v-model="model.language" :api-endpoint="this.$api.e.projectsAvailableLanguages" variant="form" align="start" label-field="language" value-field="language"> </ModelCombobox>
                </InlineField>
            </InlineFieldGroup>
            <InlineFieldGroup>
                <InlineField label="Company">
                    <ModelCombobox v-model="model.company" :api-endpoint="this.$api.e.companyList" align="start" label="Company" label-field="name" value-field="pk">
                        <template #trigger="{ label }">
                            <Button class="justify-between" role="combobox" variant="outline">
                                {{ model.company ? label : 'Select a company...' }}
                                <i class="ml-2 h-4 w-4 shrink-0 opacity-50 fa fa-chevron-down" />
                            </Button>
                        </template>
                    </ModelCombobox>
                </InlineField>
                <InlineField label="Visibility">
                    <Select v-model="model.visibility" :options="projectVisibilityChoices()" optionLabel="label" optionValue="value"></Select>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Require CVSS Score">
                <Select v-model="model.require_cvss_score" :options="scoreChoices"></Select>
            </Field>
            <Field label="Description">
                <Textarea v-model="model.description" autoResize cols="30" rows="5"></Textarea>
            </Field>
            <Button :loading="loading" class="w-full" label="Save" @click="save"></Button>
        </Form>
        <div v-else>
            <DefaultSkeleton></DefaultSkeleton>
        </div>
    </ContainerLayout>
</template>
