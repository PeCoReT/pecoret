<script>
import AuthService from '@/service/AuthService'
import { useAuthStore } from "@/store/auth";


export default {
    name: 'ResetPassword',
    data() {
        return {
            model: {
                email: null
            },
            loading: false,
            service: new AuthService(),
            authStore: useAuthStore()
        }
    },
    methods: {
        resetPassword(){
            this.loading = true
            let data = {
                email: this.model.email
            }
            this.service.resetPassword(this.$api, data).then((response) => {
                this.authStore.unsetMe();
                this.$toast.add({
                    severity: 'success',
                    summary: 'Password Reset',
                    detail: 'Check your inbox for further instructions!',
                    life: 3000
                })

            }).finally(() => {this.loading = false})
        }
    }
}
</script>

<template>
    <Toast></Toast>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <img src="/images/logo-icon.svg" alt="PeCoReT logo" class="mb-5 flex-shrink-0" />
            <div
                style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card pt-5 pb-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <span class="text-600 font-bold" style="font-size: large">Reset Password</span>
                    </div>

                    <div>
                        <label for="username" class="block text-900 text-xl font-medium mb-2">E-Mail</label>
                        <InputText id="email" type="text" placeholder="email" class="w-full md:w-30rem mb-5"
                            style="padding: 1rem" v-model="model.email" />

                        <div class="flex align-items-center justify-content-between mb-5 gap-5">
                            <a class="font-medium no-underline ml-2 text-right cursor-pointer"
                                @click="this.$router.push({name: 'Login'})"
                                style="color: var(--primary-color)">Back to Login?</a>
                        </div>
                        <Button :loading=loading label="Reset Password" class="w-full p-3 text-xl" @click="resetPassword"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
