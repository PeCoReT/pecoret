<script>
import { useAuthStore } from '@/store/auth';
import AuthLayout from '@/layout/AuthLayout.vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default {
    name: 'Login',
    components: { AuthLayout, Button, Input },

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
                email: this.email
            };
            this.$api
                .post(this.$api.e.authResetPassword, null, data)
                .then(() => {
                    this.authStore.unsetMe();
                    this.$toaster({
                        title: 'Password Reset',
                        description: 'Check your inbox for further instructions!',
                        duration: 3000
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
        <Input id="username" v-model="email" class="w-full mb-6" placeholder="Email address" />

        <div class="flex items-center justify-between mt-2 mb-6 gap-8">
            <div class="flex items-center">
                <label for="rememberme1"></label>
            </div>
            <a class="font-medium no-underline ml-2 text-right cursor-pointer text-muted-color" @click="this.$router.push({ name: 'Login' })">Back to Login</a>
        </div>
        <Button :loading="loading" class="w-full" label="Sign In" @click="resetPassword">Submit</Button>
    </AuthLayout>
</template>
