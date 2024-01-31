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
    <AuthLayout title="Sign in to continue">
        <div class="grid p-fluid formgrid">
            <div class="col-12 field">
                <label for="username" class="text-900 text-xl font-medium mb-2 mt-3">Username</label>
                <InputText id="username" type="text" placeholder="Username" class="mb-3" style="padding: 1rem" v-model="username" />
            </div>
            <div class="col-12 field">
                <label for="password" class="text-900 font-medium text-xl">Password</label>
                <Password id="password" v-model="password" placeholder="Password" :feedback="false" v-on:keyup.enter="login" :toggleMask="true" class="mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }"></Password>
            </div>
        </div>

        <div class="flex align-items-center justify-content-between mb-5 gap-5">
            <a class="font-medium no-underline ml-2 text-right cursor-pointer" @click="this.$router.push({ name: 'ResetPassword' })" style="color: var(--primary-color)">Forgot password?</a>
        </div>
        <Button :loading="loading" label="Sign In" class="w-full p-3 text-xl" @click="login"></Button>
    </AuthLayout>
</template>