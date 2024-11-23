<script>

export default {
    name: 'VersionHistoryCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            model: {
                version: null,
                change: null,
                date: null
            },
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
            let data = {
                change: this.model.change,
                date: this.model.date.toISOString().split('T')[0],
                version: this.model.version
            };
            this.$api
                .post(
                    this.$api.e.pReportVersionHistoryList,
                    {
                        pPk: this.projectId,
                        rPk: this.reportId
                    },
                    data
                )
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Version added!',
                        life: 3000,
                        detail: 'Version added to report!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Change History" outlined @click="open"></Button>

    <ModalDialog header="Add Change" v-model="visible" v-model:loading="loading" @onSave="create">
        <Form>
            <Field label="Version">
                <InputText id="version" v-model="model.version"></InputText>
            </Field>
            <Field label="Change">
                <InputText id="change" v-model="model.change"></InputText>
            </Field>
            <Field label="Date">
                <DatePicker v-model="model.date"></DatePicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
