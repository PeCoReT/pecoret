<script>

export default {
    name: 'ReportDocumentCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            loading: false,
            model: {
                name: null,
                release_type: null
            },
            releaseTypeChoices: [
                { title: 'Draft', value: 'Draft' },
                { title: 'Final', value: 'Final' }
            ],
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
            let data = {
                name: this.model.name,
                release_type: this.model.release_type
            };
            this.$api.post(this.$api.e.pReportDocumentList, {pPk: this.projectId, rPk: this.reportId}, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Document created!',
                    life: 3000,
                    detail: 'New document created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Document" outlined @click="open"></Button>

    <ModalDialog header="Create Document" v-model="visible" v-model:loading="loading" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText id="name" v-model="model.name"></InputText>
            </Field>
            <Field label="Release Type">
                <Select v-model="model.release_type" id="release_type" :options="releaseTypeChoices" optionLabel="title" optionValue="value"></Select>
            </Field>
        </Form>
    </ModalDialog>
</template>
