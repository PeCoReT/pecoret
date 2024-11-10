<script>

export default {
    name: 'UserAccountCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            loading: false,
            model: {
                username: null,
                password: null,
                role: null,
                compromised: false,
                description: ''
            },
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
                username: this.model.username,
                password: this.model.password,
                role: this.model.role,
                compromised: this.model.compromised,
                description: this.model.description
            };
            this.$api
                .post(this.$api.e.pAccountList, { projectPk: this.projectId }, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Account added!',
                        life: 3000,
                        detail: 'Account added to project!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Account" outlined @click="open"></Button>

    <ModalDialog header="Create Account" v-model="visible" v-model:loading="loading" @onSave="create">
        <Form>
            <Field label="Username">
                <InputText id="username" v-model="model.username"></InputText>
            </Field>
            <Field label="Password">
                <Password v-model="model.password" :feedback="false" toggleMask :pt="{ pcInput: { root: 'grow' } }"></Password>
            </Field>
            <Field label="Role">
                <InputText id="role" v-model="model.role"></InputText>
            </Field>
            <Field label="Description">
                <InputText v-model="model.description"></InputText>
            </Field>
            <Field>
                <div class="flex items-center">
                    <Checkbox v-model="model.compromised" :binary="true"></Checkbox>
                    <label class="ml-2">Compromised?</label>
                </div>
            </Field>
        </Form>
    </ModalDialog>
</template>
