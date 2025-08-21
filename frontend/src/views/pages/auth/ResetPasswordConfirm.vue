<script>
import AuthLayout from '@/layout/AuthLayout.vue';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ReloadIcon } from '@radix-icons/vue';

export default {
    name: 'ResetPasswordConfirm',
    components: { ReloadIcon, AuthLayout, Input, Button },
    data() {
        return {
            model: {
                password: null,
                password1: null
            },
            loading: false
        };
    },
    methods: {
        confirm() {
            this.loading = true;
            let data = {
                key: this.$route.params.token,
                password: this.model.password
            };
            this.$api
                .post(this.$api.e.authResetPasswordConfirm, null, data)
                .then(() => {
                    this.$toaster({
                        duration: 3000,
                        description: 'Password changed successfully!',
                        title: 'Password Changed!'
                    });
                    this.$router.push({ name: 'Login' });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <AuthLayout title="Activate Account">
        <Form>
            <Field>
                <Input v-model="model.password" placeholder="Password" type="password"></Input>
            </Field>
            <Field>
                <Input id="password1" v-model="model.password1" placeholder="Password confirm" type="password"></Input>
            </Field>
            <Button :disabled="model.password !== model.password1 || model.password === null" class="w-full" @click="confirm">
                <ReloadIcon v-if="loading" class="w-4 h-4 mr-2 animate-spin"></ReloadIcon>
                Change Password
            </Button>
        </Form>
    </AuthLayout>
</template>
