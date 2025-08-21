<script>
import { ModalDialog } from '@/components/dialog';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';

export default {
    name: 'UserAccountUpdateDialog',
    components: { ModalDialog, Input, Checkbox },
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
            model: this.account
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
    <Button icon="fa fa-pen-to-square" outlined size="small" @click="open"></Button>

    <ModalDialog v-model="visible" v-model:loading="loading" header="Update User Account" @onSave="patch">
        <Form>
            <Field label="Username">
                <Input id="username" v-model="model.username"></Input>
            </Field>
            <Field label="Password">
                <Input v-model="model.password" type="password"></Input>
            </Field>
            <Field label="Role">
                <Input id="role" v-model="model.role"></Input>
            </Field>
            <Field label="Description">
                <Input v-model="model.description"></Input>
            </Field>
            <Field>
                <div class="flex items-center">
                    <Checkbox v-model:checked="model.compromised"></Checkbox>
                    <label class="ml-2">Compromised?</label>
                </div>
            </Field>
        </Form>
    </ModalDialog>
</template>
