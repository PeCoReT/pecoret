<script>
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { Button } from '@/components/ui/button';

export default {
    name: 'UserAccountCreate',
    components: { BaseLayout, Input, Checkbox, Button },
    data() {
        return {
            projectId: this.$route.params.projectId,
            loading: false,
            model: {
                username: null,
                password: null,
                role: null,
                compromised: false,
                description: ''
            }
        };
    },
    methods: {
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
                .then(() => {
                    this.$toaster({
                        title: 'Account added!',
                        duration: 3000,
                        detail: 'Account added to project!'
                    });
                    this.$router.push({ name: 'UserAccountList', params: { projectId: this.projectId } });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <BaseLayout>
        <Card class="col-span-12">
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
                <Button class="w-full" @click="create">Save</Button>
            </Form>
        </Card>
    </BaseLayout>
</template>
