<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import ReportTabMenu from '@/components/projects/reporting/ReportTabMenu.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ReportTemplateSelectField from '@/components/forms/fields/ReportTemplateSelectField.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';

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
            authorChoices: [],
            saveLoading: false
        };
    },
    mounted() {
        this.getItem();
        this.$api.get('projectDetail', { pk: this.projectId }).then((response) => {
            this.project = response.data;
        });
    },
    methods: {
        getItem() {
            this.$api.get(this.$api.e.pReportDetail, { pPk: this.projectId, pk: this.reportId }).then((response) => {
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
            this.$api
                .patch(this.$api.e.pReportDetail, { pPk: this.projectId, pk: this.reportId }, data)
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
                    this.$api.delete(this.$api.e.pReportDetail, { pPk: this.projectId, pk: this.reportId }).then(() => {
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
    components: { InlineFieldGroup, ReportTemplateSelectField, DetailCardWithIcon, ReportTabMenu, MarkdownEditor }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid mt-3">
        <div class="col-span-6"></div>
        <div class="col-span-6">
            <div class="flex justify-end">
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>

    <div class="grid mt-3">
        <div class="col-span-12">
            <ReportTabMenu></ReportTabMenu>
            <div class="card border-noround-top">
                <Form class="mt-3">
                    <InlineFieldGroup>
                        <InlineField label="Name">
                            <InputText id="name" v-model="report.name"></InputText>
                        </InlineField>
                        <InlineField label="Title">
                            <InputText id="title" v-model="report.title"></InputText>
                        </InlineField>
                        <InlineField label="Author">
                            <Select id="author" optionLabel="username" :options="authorChoices" v-model="report.author" @focus="getAuthorChoices"></Select>
                        </InlineField>
                        <InlineField label="Report Template">
                            <ReportTemplateSelectField v-model="report.template"></ReportTemplateSelectField>
                        </InlineField>
                    </InlineFieldGroup>
                    <Field label="Evaluation">
                        <MarkdownEditor v-model="report.evaluation"></MarkdownEditor>
                    </Field>
                    <Field label="Recommendation">
                        <MarkdownEditor v-model="report.recommendation"></MarkdownEditor>
                    </Field>

                    <Button label="Save" @click="updateReport" :loading="saveLoading === true" class="mt-3 w-full"></Button>
                </Form>
            </div>
        </div>
    </div>
</template>
