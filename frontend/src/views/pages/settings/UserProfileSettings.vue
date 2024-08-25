<script>
import SettingsTabMenu from '@/components/navigation/SettingsTabMenu.vue';

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
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <SettingsTabMenu></SettingsTabMenu>
            <Card>
                <template #title>General</template>
                <template #content>
                    <Form>
                        <Field label="First Name">
                            <InputText v-model="model.first_name"></InputText>
                        </Field>
                        <Field label="Last Name">
                            <InputText v-model="model.last_name"></InputText>
                        </Field>
                    </Form>
                </template>
                <template #footer>
                    <div class="flex justify-end mt-3">
                        <Button @click="patch" label="Save"></Button>
                    </div>
                </template>
            </Card>
        </div>
    </div>

    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <Card>
                <template #title>Change Email</template>
                <template #content>
                    <Form>
                        <Field label="Password">
                            <Password v-model="new_email.password" :feedback="false" :pt="{ pcInput: { root: 'grow' } }"></Password>
                        </Field>
                        <Field label="New Email">
                            <InputText v-model="new_email.mail" id="new_user-help"></InputText>
                            <small id="new_user-help">Current: {{ this.model.email }}.</small>
                        </Field>
                    </Form>
                </template>
                <template #footer>
                    <div class="flex justify-end mt-3">
                        <Button @click="changeEmail" label="Save"></Button>
                    </div>
                </template>
            </Card>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <Card>
                <template #title>Change Password</template>
                <template #content>
                    <Form>
                        <Field label="Current Password">
                            <Password v-model="change_password.old_password" :feedback="false" :pt="{ pcInput: { root: 'grow' } }"></Password>
                        </Field>
                        <Field label="New Password">
                            <Password v-model="change_password.new_password" :feedback="false" :pt="{ pcInput: { root: 'grow' } }"></Password>
                        </Field>
                        <Field label="New Password (confirm)">
                            <Password v-model="change_password.new_password_confirm" :feedback="false" :pt="{ pcInput: { root: 'grow' } }"></Password>
                        </Field>
                    </Form>
                </template>
                <template #footer>
                    <div class="flex justify-end mt-3">
                        <Button @click="changePassword" label="Save" :disabled="change_password.new_password === null || change_password.new_password !== change_password.new_password_confirm"></Button>
                    </div>
                </template>
            </Card>
        </div>
    </div>
</template>
