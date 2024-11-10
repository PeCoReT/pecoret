<script>

export default {
    name: 'ProjectScopeCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                details: null,
                permission: null
            },
            loading: false,
            permissionChoices: [
                {
                    label: 'Allowed',
                    value: 'Allowed'
                },
                {
                    label: 'Denied',
                    value: 'Denied'
                }
            ]
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
                details: this.model.details,
                permission: this.model.permission
            };
            this.$api.post(this.$api.e.pScopeList, { projectPk: this.projectId }, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Scope Created!',
                    life: 3000,
                    detail: 'Scope created successfully!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Scope" outlined @click="open"></Button>

    <ModalDialog header="Create Scope" v-model="visible" v-model:loading="loading" @onSave="create">
        <Form>
            <Field label="Details">
                <InputText v-model="model.details"></InputText>
            </Field>
            <Field label="Permission">
                <Select option-label="label" option-value="value" v-model="model.permission" :options="permissionChoices"></Select>
            </Field>
        </Form>
    </ModalDialog>
</template>
