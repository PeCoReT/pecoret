<script>
import AuthService from '@/service/AuthService';
import { useAuthStore } from '@/store/auth';
import AuthLayout from '@/layout/AuthLayout.vue';

export default {
    name: 'ResetPassword',
    components: { AuthLayout },
    data() {
        return {
            model: {
                email: null
            },
            loading: false,
            service: new AuthService(),
            authStore: useAuthStore()
        };
    },
    methods: {
        resetPassword() {
            this.loading = true;
            let data = {
                email: this.model.email
            };
            this.service
                .resetPassword(this.$api, data)
                .then(() => {
                    this.authStore.unsetMe();
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Password Reset',
                        detail: 'Check your inbox for further instructions!',
                        life: 3000
                    });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <AuthLayout title="Reset Password">
        <div class="grid formgrid p-fluid">
            <div class="col-12 field">
                <label for="username" class="text-900 text-xl font-medium mb-2">E-Mail</label>
                <InputText id="email" type="text" placeholder="email" class="mb-3" style="padding: 1rem" v-model="model.email" />
            </div>
        </div>
        <div class="flex align-items-center justify-content-between mb-5 gap-5">
            <a class="font-medium no-underline ml-2 text-right cursor-pointer" @click="this.$router.push({ name: 'Login' })" style="color: var(--primary-color)">Back to Login?</a>
        </div>
        <Button :loading="loading" label="Reset Password" class="w-full p-3 text-xl" @click="resetPassword"></Button>
    </AuthLayout>
</template>