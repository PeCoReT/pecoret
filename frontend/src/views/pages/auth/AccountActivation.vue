<script>
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
            this.$api
                .post(this.$api.e.authActivation, null, data)
                .then(() => {
                    this.$toaster({
                        duration: 3000,
                        description: 'Account activated successfully!',
                        title: 'Account Activated!'
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
        <Fluid>
            <div class="col-12 field mb-6">
                <Password id="password" v-model="model.password" :feedback="false" :toggleMask="true" inputClass="w-full" placeholder="Password"></Password>
            </div>
            <div class="col-12 field mb-6">
                <Password id="password1" v-model="model.password1" :feedback="false" :toggleMask="true" class="w-full mb-3" inputClass="w-full" placeholder="Password confirm"></Password>
            </div>
        </Fluid>
        <Button :disabled="model.password !== model.password1 || model.password === null" :loading="loading" class="w-full p-3 text-xl" label="Change Password" @click="activateAccount"></Button>
    </AuthLayout>
</template>
