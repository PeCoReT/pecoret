<script>
import { useAuthStore } from '@/store/auth';
import AuthLayout from '@/layout/AuthLayout.vue';

export default {
    name: 'Login',
    components: { AuthLayout },

    data() {
        return {
            email: null,
            loading: false,
            authStore: useAuthStore()
        };
    },
    methods: {
        resetPassword() {
            this.loading = true;
            let data = {
                email: this.model.email
            };
            this.$api
                .post('authResetPassword', null, data)
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
    <AuthLayout>
        <InputText id="username" type="text" placeholder="Email address" class="w-full mb-6" v-model="email" />

        <div class="flex items-center justify-between mt-2 mb-6 gap-8">
            <div class="flex items-center">
                <label for="rememberme1"></label>
            </div>
            <a @click="this.$router.push({ name: 'Login' })" class="font-medium no-underline ml-2 text-right cursor-pointer text-primary">Forgot password?</a>
        </div>
        <Button :loading="loading" label="Sign In" class="w-full" @click="resetPassword"></Button>
    </AuthLayout>
</template>
