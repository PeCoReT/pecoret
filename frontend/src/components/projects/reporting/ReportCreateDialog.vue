<script>
import ReportTemplateSelectField from '@/components/forms/fields/ReportTemplateSelectField.vue';

export default {
    name: 'ReportCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                template: null,
                author: null
            },
            templateChoices: null,
            loading: false,
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        create() {
            this.loading = true;
            let data = {
                name: this.model.name,
                template: this.model.template,
            };
            this.$api
                .post(this.$api.e.pReportList, { pPk: this.projectId }, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Report created!',
                        life: 3000,
                        detail: 'New report created!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { ReportTemplateSelectField }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Report" outlined @click="open"></Button>

    <ModalDialog header="Create Report" v-model="visible" :loading="loading" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText id="name" v-model="model.name"></InputText>
            </Field>
            <Field label="Report Template">
                <ReportTemplateSelectField v-model="model.template"></ReportTemplateSelectField>
            </Field>
        </Form>
    </ModalDialog>
</template>
