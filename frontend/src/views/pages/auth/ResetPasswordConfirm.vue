<script>
import AuthLayout from '@/layout/AuthLayout.vue';

export default {
    name: 'ResetPasswordConfirm',
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
        confirm() {
            this.loading = true;
            let data = {
                uid: this.$route.params.uid,
                token: this.$route.params.token,
                new_password: this.model.password
            };
            this.$api
                .post(this.$api.e.authResetPasswordConfirm, null, data)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        life: 3000,
                        detail: 'Account activated successfully!',
                        summary: 'Account Activated!'
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
                <Password id="password" v-model="model.password" placeholder="Password" :feedback="false" :toggleMask="true" inputClass="w-full"></Password>
            </div>
            <div class="col-12 field mb-6">
                <Password id="password1" v-model="model.password1" placeholder="Password confirm" :feedback="false" :toggleMask="true" class="w-full mb-3" inputClass="w-full"></Password>
            </div>
        </Fluid>
        <Button :loading="loading" label="Change Password" class="w-full p-3 text-xl" @click="confirm" :disabled="model.password !== model.password1 || model.password === null"></Button>
    </AuthLayout>
</template>
