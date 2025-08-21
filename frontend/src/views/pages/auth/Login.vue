<script>
import { useAuthStore } from '@/store/auth';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import AuthLayout from '@/layout/AuthLayout.vue';

export default {
    name: 'Login',
    components: { AuthLayout, Input, Button },
    mounted() {
        this.$api.get(this.$api.e.authCheck).then((response) => {
            this.authStore.setAuthData(response.data);
        });

        if (this.authStore.is_authenticated === true) {
            this.$router.push({ name: 'ProjectList' });
        }
        this.$api.get(this.$api.e.authConfig).then((response) => {
            this.providers = response.data.data.socialaccount.providers;
        });
    },
    computed: {
        callbackUrl() {
            return window.location.href.split('#')[0];
        }
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
        <Input id="username" v-model="username" class="w-full mb-6" placeholder="Username" type="text" />
        <Input id="password" v-model="password" :feedback="false" class="mb-4" fluid placeholder="Password" type="password" v-on:keyup.enter="login"></Input>

        <div class="flex items-center justify-between mt-2 mb-6 gap-8">
            <div class="flex items-center">
                <label for="rememberme1"></label>
            </div>
            <a class="font-medium no-underline ml-2 text-right cursor-pointer" @click="this.$router.push({ name: 'ResetPassword' })">Forgot password?</a>
        </div>
        <Button :loading="loading" class="w-full" @click="login">Login</Button>

        <div class="mt-3">
            <div v-for="provider in providers" :key="provider.id">
                <form :action="`/api${this.$api.e.authProviderRedirect}`" method="POST">
                    <input :value="this.authStore.csrfToken" name="csrfmiddlewaretoken" type="hidden" />
                    <input :value="provider.id" name="provider" type="hidden" />
                    <input :value="callbackUrl" name="callback_url" type="hidden" />
                    <input name="process" type="hidden" value="login" />
                    <Button class="w-full" type="submit">Login with {{ provider.name }}</Button>
                </form>
            </div>
        </div>
    </AuthLayout>
</template>
