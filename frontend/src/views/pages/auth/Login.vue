<script>
import AuthService from '@/service/AuthService';
import { useAuthStore } from '@/store/auth';
import AuthLayout from '@/layout/AuthLayout.vue';

export default {
    name: 'Login',
    components: { AuthLayout },
    mounted() {
        this.service.checkAuth(this.$api);
        if (this.authStore.me) {
            if (this.authStore.groups.isVendor === true) {
                this.$router.push({ name: 'AdvisoryList' });
            } else if (this.authStore.groups.isAdmin === true) {
                this.$router.push({
                    name: 'AdminSettings'
                });
            } else {
                this.$router.push({ name: 'ProjectList' });
            }
        }
    },
    data() {
        return {
            service: new AuthService(),
            authStore: useAuthStore(),
            username: null,
            password: null,
            loading: false
        };
    },
    methods: {
        login() {
            this.loading = true;
            this.service
                .login(this.$api, this.username, this.password)
                .then((response) => {
                    this.authStore.setAuthData(response.data);
                    if (this.authStore.groups.isVendor === true) {
                        this.$router.push({ name: 'AdvisoryList' });
                    } else if (this.authStore.groups.isAdmin === true) {
                        this.$router.push({
                            name: 'AdminSettings'
                        });
                    } else {
                        this.$router.push({ name: 'ProjectList' });
                    }
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
        <InputText id="username" type="text" placeholder="Username" class="w-full mb-6" v-model="username" />
        <Password id="password" v-model="password" placeholder="Password" :toggleMask="true" class="mb-4" fluid v-on:keyup.enter="login" :feedback="false"></Password>

        <div class="flex items-center justify-between mt-2 mb-6 gap-8">
            <div class="flex items-center">
                <label for="rememberme1"></label>
            </div>
            <a @click="this.$router.push({ name: 'ResetPassword' })" class="font-medium no-underline ml-2 text-right cursor-pointer text-primary">Forgot password?</a>
        </div>
        <Button :loading="loading" label="Sign In" class="w-full" @click="login"></Button>
    </AuthLayout>
</template>
