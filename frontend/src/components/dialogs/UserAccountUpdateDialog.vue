<script>

export default {
    name: 'UserAccountUpdateDialog',
    props: {
        account: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            loading: false,
            model: this.account,
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        patch() {
            this.loading = true;
            let data = {
                username: this.model.username,
                password: this.model.password,
                role: this.model.role,
                compromised: this.model.compromised,
                description: this.model.description
            };
            this.$api
                .patch(
                    this.$api.e.pAccountDetail,
                    {
                        projectPk: this.$route.params.projectId,
                        pk: this.account.pk
                    },
                    data
                )
                .then(() => {
                    this.$emit('object-updated', this.model);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    watch: {
        account: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <ModalDialog header="Update User Account" v-model="visible" v-model:loading="loading" @onSave="patch">
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
