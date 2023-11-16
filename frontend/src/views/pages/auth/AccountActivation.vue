<script>
import AuthService from '@/service/AuthService';
import AuthLayout from '@/layout/AuthLayout.vue';

export default {
    name: 'AccountActivation',
    components: { AuthLayout },
    data() {
        return {
            model: {
                password: null,
                password1: null
            },
            service: new AuthService(),
            loading: false
        };
    },
    methods: {
        activateAccount() {
            this.loading = true;
            let data = {
                uid: this.$route.params.uid,
                token: this.$route.params.token,
                new_password: this.model.password
            };
            this.service
                .activateAccount(this.$api, data)
                .then(() => {
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
        <div class="formgroup p-fluid grid">
            <div class="col-12 field">
                <label for="password" class="text-900 text-xl font-medium mb-2">Password</label>
                <Password id="password" v-model="model.password" placeholder="Password" :feedback="false" :toggleMask="true" inputClass="w-full" :inputStyle="{ padding: '1rem' }"></Password>
            </div>
            <div class="col-12 field">
                <label for="password1" class="block text-900 font-medium text-xl mb-2">Password (confirm)</label>
                <Password id="password1" v-model="model.password1" placeholder="Password" :feedback="false" :toggleMask="true" class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }"></Password>
            </div>
        </div>
        <Button :loading="loading" label="Change Password" class="w-full p-3 text-xl" @click="activateAccount" :disabled="model.password !== model.password1 || model.password === null"></Button>
    </AuthLayout>
</template>