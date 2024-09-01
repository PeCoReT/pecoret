<script>
import PentestTypeSelectField from '@/components/forms/fields/PentestTypeSelectField.vue';
import CompanyService from '@/service/CompanyService';
import ProjectService from '@/service/ProjectService';
import { useAuthStore } from '@/store/auth';
import CompanySelectField from '@/components/forms/fields/CompanySelectField.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';
import InlineField from '@/components/common/forms/InlineField.vue';

export default {
    name: 'ProjectUpdateDialog',
    props: {
        project: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            showDialog: false,
            loading: false,
            authStore: useAuthStore(),
            model: this.project,
            projectId: this.$route.params.projectId,
            companyService: new CompanyService(),
            service: new ProjectService(),
            availableLanguages: [],
            companyChoices: null,
            testMethodChoices: [
                { title: 'Unknown', value: 'Unknown' },
                { title: 'Greybox', value: 'Grey Box' },
                { title: 'Blackbox', value: 'Black Box' },
                { title: 'Whitebox', value: 'White Box' }
            ],
            scoreChoices: [
                { label: 'CVSS 4.0 Base', value: 0 },
                { label: 'CVSS 3.1 Base', value: 1 }
            ]
        };
    },
    mounted() {
        this.getLanguages();
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        getLanguages() {
            let url = '/projects/available-languages/';
            this.$api.get(url).then((response) => {
                this.availableLanguages = response.data;
            });
        },
        save() {
            this.loading = true;
            if (typeof this.model.pentest_types === 'object') {
                if (this.model.pentest_types.length > 0) {
                    if (this.model.pentest_types[0].pk) {
                        delete this.model.pentest_types;
                    }
                }
            }
            let data = {
                pentest_types: this.model.pentest_types,
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
            if (this.model.company && this.model.company.pk) {
                data['company'] = this.model.company.pk;
            }
            this.service
                .patchProject(this.$api, this.projectId, data)
                .then(() => {
                    this.authStore.activateProject(this.model);
                    this.$emit('object-updated', this.model);
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    watch: {
        project: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
                if (this.model.company && this.model.company.pk && !this.companyChoices) {
                    this.companyChoices = [this.model.company];
                }
            }
        }
    },
    components: { InlineField, InlineFieldGroup, ModalDialog, CompanySelectField, PentestTypeSelectField }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" label="Edit" @click="open()" outlined></Button>

    <ModalDialog v-model:loading="loading" header="Edit Project" v-model="showDialog" @onSave="save">
        <Form>
            <Field label="Name">
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
                <InlineField label="Project Types">
                    <PentestTypeSelectField v-model="model.pentest_types"></PentestTypeSelectField>
                </InlineField>
                <InlineField label="Language">
                    <Select optionLabel="language" optionValue="language" v-model="model.language" :options="availableLanguages"></Select>
                </InlineField>
            </InlineFieldGroup>
            <InlineFieldGroup>
                <InlineField label="Company">
                    <CompanySelectField v-model="model.company" :clear="false"></CompanySelectField>
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
