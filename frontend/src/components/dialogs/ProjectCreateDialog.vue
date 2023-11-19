<script>
import ProjectService from '@/service/ProjectService';
import CompanyService from '@/service/CompanyService';
import PentestTypeSelectField from '../elements/forms/PentestTypeSelectField.vue';

export default {
    name: 'ProjectCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            model: {
                pentest_types: null,
                name: null,
                start_date: null,
                end_date: null,
                test_method: null,
                language: null,
                description: '',
                require_cvss_score: null,
                company: null
            },
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
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
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
        getCompanies() {
            this.companyService.getCompanies().then((response) => {
                this.companyChoices = response.data.results;
            });
        },
        create() {
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
                company: this.model.company
            };
            this.service.createProject(this.$api, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created',
                    life: 3000,
                    detail: 'Project created successfully!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    },
    components: { PentestTypeSelectField }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Project" @click="open()" outlined></Button>

    <Dialog header="Create Project" v-model:visible="visible" :breakpoints="{ '960px': '75vw' }" :style="{ width: '70vw' }" :modal="true">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name" label="Name"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="start_date">Start Date</label>
                <Calendar v-model="model.start_date"></Calendar>
            </div>
            <div class="field col-12 md:col-6">
                <label for="end_date">End Date</label>
                <Calendar v-model="model.end_date"></Calendar>
            </div>
            <div class="field col-12">
                <label for="test_method">Test Method</label>
                <Dropdown v-model="model.test_method" :options="testMethodChoices" optionLabel="title" optionValue="value"></Dropdown>
            </div>
            <div class="field col-12 md:col-6">
                <PentestTypeSelectField v-model="model.pentest_types"></PentestTypeSelectField>
            </div>
            <div class="field col-12 md:col-6">
                <label for="language">Language</label>
                <Dropdown optionLabel="language" optionValue="language" @focus="onFocusLanguages" v-model="model.language" :options="languageChoices"></Dropdown>
            </div>

            <div class="field col-12">
                <label for="company">Company</label>
                <Dropdown :options="companyChoices" @filter="onFilterCompany" @focus="onFocusCompany" filter optionLabel="name" optionValue="pk" v-model="model.company"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="require_cvss_score">Require CVSS Score</label>
                <Dropdown :options="scoreChoices" :show-clear="true" optionLabel="label" optionValue="value" v-model="model.require_cvss_score"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <Textarea v-model="model.description" autoResize rows="5" cols="30"></Textarea>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>