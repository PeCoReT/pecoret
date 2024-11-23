<script>
import { useAuthStore } from '@/store/auth';
import AuthLayout from '@/layout/AuthLayout.vue';

export default {
    name: 'Login',
    components: { AuthLayout },
    mounted() {
        this.$api.get(this.$api.e.authCheck).then((response) => {
            this.authStore.setAuthData(response.data);
        });

        if (this.authStore.me) {
            this.$router.push({ name: 'ProjectList' });
        }
        this.$api.get(this.$api.e.authConfig).then((response) => {
            this.providers = response.data.data.socialaccount.providers;
        });
    },
    computed: {
        callbackUrl() {
            return window.location.href.split('#')[0];
        },
    },
    data() {
        return {
            authStore: useAuthStore(),
            username: null,
            password: null,
            loading: false,
            providers: []
        };
    },
    methods: {
        login() {
            this.loading = true;
            this.authStore.unsetMe();
            this.$api
                .post(this.$api.e.authLogin, null, { username: this.username, password: this.password })
                .then((response) => {
                    this.authStore.setAuthData(response.data);
                    this.$router.push({ name: 'ProjectList' });
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
        <Button :loading="loading" label="Login" class="w-full" @click="login"></Button>

        <div class="mt-3">
            <div v-for="provider in providers" :key="provider.id">
                <form :action="`/api${this.$api.e.authProviderRedirect}`" method="POST">
                    <input type="hidden" :value="this.authStore.csrfToken" name="csrfmiddlewaretoken">
                    <input type="hidden" :value="provider.id" name="provider" />
                    <input type="hidden" :value="callbackUrl" name="callback_url" />
                    <input type="hidden" value="login" name="process" />
                    <Button class="w-full" type="submit">Login with {{ provider.name }}</Button>
                </form>
            </div>
        </div>
    </AuthLayout>
</template>
