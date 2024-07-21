<script>
import ReportService from '@/service/ReportService';
import ProjectService from '@/service/ProjectService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import ReportTabMenu from '@/components/projects/reporting/ReportTabMenu.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ReportTemplateSelectField from "@/components/elements/forms/ReportTemplateSelectField.vue";

export default {
    name: 'ReportDetail',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Reports',
                    to: this.$router.resolve({
                        name: 'ReportList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Report Detail',
                    disabled: true
                }
            ],
            report: { author: {}, template: {} },
            project: {},
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            reportService: new ReportService(),
            projectService: new ProjectService(),
            authorChoices: [],
            saveLoading: false
        };
    },
    mounted() {
        this.getItem();
        this.projectService.getProject(this.projectId).then((response) => {
            this.project = response.data;
        });
    },
    methods: {
        getItem() {
            this.reportService.getReport(this.$api, this.projectId, this.reportId).then((response) => {
                this.report = response.data;
                this.authorChoices.push(this.report.author);
            });
        },
        updateReport() {
            this.saveLoading = true;
            let data = {
                title: this.report.title,
                name: this.report.name,
                recommendation: this.report.recommendation,
                evaluation: this.report.evaluation,
                template: this.report.template
            };
            this.reportService
                .updateReport(this.$api, this.projectId, this.reportId, data)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Report updated!',
                        life: 3000,
                        detail: 'Report was updated successfully!'
                    });
                    this.getItem();
                })
                .finally(() => {
                    this.saveLoading = false;
                });
        },
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this report?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.reportService.deleteReport(this.$api, this.projectId, this.reportId).then(() => {
                        this.$router.push({ name: 'ReportList', params: { projectId: this.projectId } });
                    });
                }
            });
        },
        getAuthorChoices() {
            let url = '/projects/' + this.projectId + '/memberships/';
            this.$api.get(url).then((response) => {
                let authors = [];
                response.data.results.forEach(function (item) {
                    authors.push(item.user);
                });
                this.authorChoices = authors;
            });
        }
    },
    components: {ReportTemplateSelectField, DetailCardWithIcon, ReportTabMenu, MarkdownEditor }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <ReportTabMenu class="surface-card"></ReportTabMenu>
            <div class="card border-noround-top">
                <div class="grid formgrid p-fluid mt-3">
                    <div class="field sm:col-12 md:col-3">
                        <label for="name">Name</label>
                        <InputText id="name" v-model="report.name"></InputText>
                    </div>
                    <div class="field sm:col-12 md:col-3">
                        <label for="title">Title</label>
                        <InputText id="title" v-model="report.title"></InputText>
                    </div>
                    <div class="field sm:col-12 md:col-3">
                        <label for="author">Author</label>
                        <Dropdown id="author" optionLabel="username" :options="authorChoices" v-model="report.author" @focus="getAuthorChoices"></Dropdown>
                    </div>
                    <div class="field sm:col-12 md:col-3">
                        <ReportTemplateSelectField v-model="report.template"></ReportTemplateSelectField>
                    </div>
                    <div class="field col-12">
                        <label for="evaluation">Evaluation</label>
                        <MarkdownEditor v-model="report.evaluation"></MarkdownEditor>
                    </div>
                    <div class="field col-12">
                        <label for="recommendation">Recommendation</label>
                        <MarkdownEditor v-model="report.recommendation"></MarkdownEditor>
                    </div>
                    <div class="col-12">
                        <div class="flex justify-content-end mt-3">
                            <Button label="Save" @click="updateReport" :loading="saveLoading === true"></Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>