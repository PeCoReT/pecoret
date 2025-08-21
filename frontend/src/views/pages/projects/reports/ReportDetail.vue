<script>
import { MarkdownEditor } from '@/components/editor';
import { DetailCardWithIcon } from '@/components/card';
import { ReportTabMenu } from '@/partials/projects';
import { Input } from '@/components/ui/input';
import { ModelCombobox } from '@/components/combobox';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'ReportDetail',
    data() {
        return {
            report: {},
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            saveLoading: false
        };
    },
    mounted() {
        this.getItem();
    },
    methods: {
        getItem() {
            this.$api.get(this.$api.e.pReportDetail, { pPk: this.projectId, pk: this.reportId }).then((response) => {
                this.report = response.data;
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
                    this.$toaster({
                        title: 'Report updated!',
                        duration: 3000,
                        description: 'Report was updated successfully!'
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
        }
    },
    components: {
        ContainerLayout,
        ModelCombobox,
        DetailCardWithIcon,
        ReportTabMenu,
        MarkdownEditor,
        Input,
        Button
    }
};
</script>
<template>
    <ContainerLayout>
        <template #right-header>
            <Button variant="destructive" @click="confirmDialogDelete"><i class="fa fa-trash"></i> Delete</Button>
        </template>
        <template #left-header>
            <ReportTabMenu class="md:max-w-lg"></ReportTabMenu>
        </template>
        <Form>
            <InlineFieldGroup>
                <InlineField label="Name">
                    <Input id="name" v-model="report.name"></Input>
                </InlineField>
                <InlineField label="Title">
                    <Input id="title" v-model="report.title"></Input>
                </InlineField>
                <InlineField label="Report Template">
                    <ModelCombobox v-model="report.template" :api-endpoint="this.$api.e.reportTemplateList" align="start" label-field="name" value-field="name" variant="form"></ModelCombobox>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Evaluation">
                <MarkdownEditor v-model="report.evaluation"></MarkdownEditor>
            </Field>
            <Field label="Recommendation">
                <MarkdownEditor v-model="report.recommendation"></MarkdownEditor>
            </Field>

            <Button class="mt-3 w-full" @click="updateReport">Save</Button>
        </Form>
    </ContainerLayout>
</template>
