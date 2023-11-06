<script>
import AuthService from '@/service/AuthService'


export default {
    name: 'AccountActivation',
    data() {
        return {
            model: {
                password: null,
                password1: null
            },
            service: new AuthService(),
            loading: false
        }
    },
    methods: {
        activateAccount(){
            this.loading = true
            let data = {
                uid: this.$route.params.uid,
                token: this.$route.params.token,
                new_password: this.model.password
            }
            this.service.activateAccount(this.$api, data).then(() => {
                this.$router.push({name: 'Login'})
            }).finally(() => { this.loading = false})
        }
    }
}
</script>

<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <img src="/images/logo-icon.svg" alt="PeCoReT logo" class="mb-5 flex-shrink-0" />
            <div
                style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card pt-5 pb-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <span class="text-600 font-bold" style="font-size: large">Activate Account</span>
                    </div>

                    <div>
                        <label for="username" class="block text-900 text-xl font-medium mb-2">Password</label>
                        <Password id="password" v-model="model.password" placeholder="Password" :feedback="false"
                            :toggleMask="true" class="w-full mb-3" inputClass="w-full" :inputStyle="{padding: '1rem'}"></Password>


                        <label for="password1" class="block text-900 font-medium text-xl mb-2">Password (confirm)</label>
                        <Password id="password1" v-model="model.password1" placeholder="Password" :feedback="false"
                            :toggleMask="true" class="w-full mb-3" inputClass="w-full" :inputStyle="{padding: '1rem'}"></Password>

                        <Button :loading=loading label="Change Password" class="w-full p-3 text-xl" @click="activateAccount" :disabled="(model.password !== model.password1) || (model.password === null)"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
