<script>
import PentestTypeSelectField from '../elements/forms/PentestTypeSelectField.vue';
import CompanyService from '@/service/CompanyService';
import ProjectService from '@/service/ProjectService';
import { useAuthStore } from "@/store/auth";

const projectService = new ProjectService();

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
            visible: false,
            loading: false,
            authStore: useAuthStore(),
            model: this.project,
            projectId: this.$route.params.projectId,
            companyService: new CompanyService(),
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
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        getCompanies() {
            this.companyService.getCompanies().then((response) => {
                this.companyChoices = response.data.results;
            });
        },
        onFocusCompany() {
            if (this.companyChoices) {
                return;
            }
            this.companyService.getCompanies().then((response) => {
                this.companyChoices = response.data.results;
            });
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
            let url = '/projects/available-languages/';
            this.$api.get(url).then((response) => {
                this.availableLanguages = response.data;
            });
        },
        getCompany() {
            this.companyService.getCompany(this.project.company).then((response) => {
                this.companyChoices = [response.data];
            });
        },
        patchProject() {
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
                company: this.model.company
            };
            projectService
                .patchProject(this.$api, this.projectId, data)
                .then(() => {
                    this.authStore.activateProject(this.model);
                    this.$emit('object-updated', this.model);
                    this.visible = false;
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
                if (this.model.company && !this.companyChoices) {
                    this.getCompany();
                }
            }
        }
    },
    components: { PentestTypeSelectField }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" label="Edit" @click="open()" outlined></Button>

    <Dialog header="Edit Project" v-model:visible="visible" :breakpoints="{ '960px': '75vw' }" :style="{ width: '70vw' }" :modal="true">
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
                <Dropdown optionLabel="language" optionValue="language" v-model="model.language" :options="availableLanguages"></Dropdown>
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
            <Button label="Save" @click="patchProject" :loading="loading" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>