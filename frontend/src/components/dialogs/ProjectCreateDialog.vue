<script>
import ProjectService from '@/service/ProjectService';
import CompanyService from '@/service/CompanyService';
import PentestTypeSelectField from '@/components/forms/fields/PentestTypeSelectField.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';

export default {
    name: 'ProjectCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                pentest_types: null,
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
            loading: false,
            scoreChoices: [
                { label: 'CVSS 4.0 Base', value: 0 },
                { label: 'CVSS 3.1 Base', value: 1 }
            ],
            testMethodChoices: [
                { title: 'Unknown', value: 'Unknown' },
                { title: 'Greybox', value: 'Grey Box' },
                { title: 'Blackbox', value: 'Black Box' },
                { title: 'Whitebox', value: 'White Box' }
            ],
            companyChoices: null,
            languageChoices: null,
            service: new ProjectService(),
            companyService: new CompanyService()
        };
    },
    mounted() {
        this.model.visibility = 'Members Only';
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        onFocusCompany() {
            if (this.companyChoices) {
                return;
            }
            this.companyService.getCompanies().then((response) => {
                this.companyChoices = response.data.results;
            });
        },
        onFocusLanguages() {
            this.getLanguages();
        },
        onFilterCompany(event) {
            let params = {
                search: event.value
            };
            this.companyService.getCompanies(params).then((response) => {
                this.companyChoices = response.data.results;
            });
        },
        getLanguages() {
            if (this.languageChoices) {
                return;
            }
            this.service.getLanguages(this.$api).then((response) => {
                this.languageChoices = response.data;
            });
        },
        create() {
            this.loading = true;
            let data = {
                pentest_types: this.model.pentest_types,
                name: this.model.name,
                start_date: this.model.start_date.toISOString().split('T')[0],
                end_date: this.model.end_date.toISOString().split('T')[0],
                status: 'Open',
                test_method: this.model.test_method,
                language: this.model.language,
                require_cvss_base_score: this.model.require_cvss_base_score,
                description: this.model.description,
                company: this.model.company,
                visibility: this.model.visibility
            };
            this.service
                .createProject(this.$api, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Created',
                        life: 3000,
                        detail: 'Project created successfully!'
                    });
                    this.$emit('object-created', response.data);
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { ModalDialog, PentestTypeSelectField }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Project" @click="open()" outlined></Button>

    <ModalDialog :loading="loading" header="New Project" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="name">
                <InputText id="name" type="text" v-model="model.name" label="Name"></InputText>
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
                <Select v-model="model.test_method" :options="testMethodChoices" optionLabel="title" optionValue="value"></Select>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Project Type">
                    <PentestTypeSelectField v-model="model.pentest_types"></PentestTypeSelectField>
                </InlineField>
                <InlineField label="Language">
                    <Select optionLabel="language" optionValue="language" @focus="onFocusLanguages" v-model="model.language" :options="languageChoices"></Select>
                </InlineField>
            </InlineFieldGroup>
            <InlineFieldGroup>
                <InlineField label="Company">
                    <Select :options="companyChoices" @filter="onFilterCompany" @focus="onFocusCompany" filter optionLabel="name" optionValue="pk" v-model="model.company"></Select>
                </InlineField>
                <InlineField label="Visibility">
                    <Select :options="service.getVisibilityChoices()" optionLabel="label" optionValue="value" v-model="model.visibility"></Select>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Require CVSS Score">
                <Select :options="scoreChoices" :show-clear="true" optionLabel="label" optionValue="value" v-model="model.require_cvss_score"></Select>
            </Field>
            <Field label="Description">
                <Textarea v-model="model.description" autoResize rows="5" cols="30"></Textarea>
            </Field>
        </Form>
    </ModalDialog>
</template>
