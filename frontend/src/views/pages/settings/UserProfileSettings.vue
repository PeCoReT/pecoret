<script>
import SettingsTabMenu from '@/components/pages/SettingsTabMenu.vue';

export default {
    name: 'UserProfileSettings',
    components: { SettingsTabMenu },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Settings',
                    disabled: true
                }
            ],
            model: {},
            new_email: {
                password: null,
                mail: null
            },
            change_password: {
                old_password: null,
                new_password: null,
                new_password_confirm: null
            }
        };
    },
    methods: {
        getItem() {
            let url = '/auth/check/';
            this.$api.get(url).then((response) => {
                this.model = response.data.user;
            });
        },
        patch() {
            let url = '/users/update_profile/';
            this.$api.patch(url, this.model).then((response) => {
                this.model = response.data;
                this.$toast.add({
                    severity: 'success',
                    summary: 'Updated',
                    detail: 'Settings were updated successfully!',
                    life: 3000
                });
            });
        },
        changePassword() {
            let url = '/users/change_password/';
            let data = {
                old_password: this.change_password.old_password,
                new_password: this.change_password.new_password
            };
            this.$api.post(url, data).then((response) => {
                this.change_password.old_password = null;
                this.change_password.new_password = null;
                this.change_password.new_password_confirm = null;
                this.$toast.add({
                    severity: 'success',
                    summary: 'Password changed',
                    life: 3000,
                    detail: response.data.message
                });
            });
        },
        changeEmail() {
            let url = '/users/change_email/';
            let data = {
                password: this.new_email.password,
                email: this.new_email.mail
            };
            this.$api.post(url, data).then((response) => {
                this.new_email.password = null;
                this.new_email.mail = null;
                this.$toast.add({
                    severity: 'success',
                    summary: 'Change Email',
                    life: 3000,
                    detail: response.data.message
                });
            });
        }
    },
    mounted() {
        this.getItem();
    }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <SettingsTabMenu class="surface-card"></SettingsTabMenu>
            <Card>
                <template #title>General</template>
                <template #content>
                    <div class="grid formgrid p-fluid">
                        <div class="field col-12">
                            <label for="first_name">First Name</label>
                            <InputText v-model="model.first_name"></InputText>
                        </div>
                        <div class="field col-12">
                            <label for="first_name">Last Name</label>
                            <InputText v-model="model.last_name"></InputText>
                        </div>
                    </div>
                </template>
                <template #footer>
                    <div class="flex justify-content-end mt-3">
                        <Button @click="patch" label="Save"></Button>
                    </div>
                </template>
            </Card>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <Card>
                <template #title>Change Email</template>
                <template #content>
                    <div class="grid formgrid p-fluid">
                        <div class="field col-12">
                            <label for="password">Password</label>
                            <Password v-model="new_email.password" :feedback="false"></Password>
                        </div>
                        <div class="field col-12">
                            <label for="new_email">New Email</label>
                            <InputText v-model="new_email.mail" id="new_user-help"></InputText>
                            <small id="new_user-help">Current: {{ this.model.email }}.</small>
                        </div>
                    </div>
                </template>
                <template #footer>
                    <div class="flex justify-content-end mt-3">
                        <Button @click="changeEmail" label="Save"></Button>
                    </div>
                </template>
            </Card>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <Card>
                <template #title>Change Password</template>
                <template #content>
                    <div class="grid formgrid p-fluid">
                        <div class="field col-12">
                            <label for="old_password">Current Password</label>
                            <Password v-model="change_password.old_password" :feedback="false"></Password>
                        </div>
                        <div class="field col-12">
                            <label for="new_password">New Password</label>
                            <Password v-model="change_password.new_password" :feedback="false"></Password>
                        </div>
                        <div class="field col-12">
                            <label for="new_password">New Password (confirm)</label>
                            <Password v-model="change_password.new_password_confirm" :feedback="false"></Password>
                        </div>
                    </div>
                </template>
                <template #footer>
                    <div class="flex justify-content-end mt-3">
                        <Button @click="changePassword" label="Save" :disabled="change_password.new_password === null || change_password.new_password !== change_password.new_password_confirm"></Button>
                    </div>
                </template>
            </Card>
        </div>
    </div>
</template>
