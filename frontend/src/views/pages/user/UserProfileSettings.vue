<script>
import UserSettingsPageLayout from '@/layout/UserSettingsPageLayout.vue';

export default {
    name: 'UserProfileSettings',
    components: { UserSettingsPageLayout },
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
            },
            menuItems: [
                {
                    label: 'Account',
                    command: () => {
                        this.$router.push({
                            name: 'UserProfileSettings'
                        })
                    }
                },
                {
                    label: 'Notifications',
                    command: () => {
                        this.$router.push({
                            name: 'UserSettingsDetail'
                        })
                    }
                }
            ]
        };
    },
    methods: {
        getItem() {
            this.$api.get(this.$api.e.authCheck).then((response) => {
                this.model = response.data.data.user;
            });
        },
        patch() {
            this.$api.patch(this.$api.e.userUpdateProfile, {}, this.model).then((response) => {
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
            let data = {
                current_password: this.change_password.old_password,
                new_password: this.change_password.new_password
            };
            this.$api.post(this.$api.e.authChangePassword, {}, data).then((response) => {
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
            let data = {
                password: this.new_email.password,
                email: this.new_email.mail
            };
            this.$api.post(this.$api.e.userChangeEmail, {}, data).then((response) => {
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
    <UserSettingsPageLayout subheadline="Update your personal data here!" headline="Account">
        <p class="font-bold text-lg mb-3">Profile</p>
        <Form>
            <Field label="First Name">
                <InputText v-model="model.first_name"></InputText>
            </Field>
            <Field label="Last Name">
                <InputText v-model="model.last_name"></InputText>
            </Field>
            <Field label="Nickname">
                <InputText v-model="model.nickname"></InputText>
            </Field>
            <Button @click="patch" label="Save" class="w-full"></Button>
        </Form>
        <hr class="mt-8 mb-8" />

        <p class="font-bold text-lg mb-3">Change E-Mail</p>
        <Form>
            <Field label="Password">
                <Password v-model="new_email.password" :fluid="true" :feedback="false" :pt="{ pcInput: { root: 'grow' } }"></Password>
            </Field>
            <Field label="New Email">
                <InputText v-model="new_email.mail" id="new_user-help"></InputText>
                <small id="new_user-help">Current: {{ this.model.email }}.</small>
            </Field>
            <Button @click="changeEmail" label="Save" class="w-full"></Button>
        </Form>

        <hr class="mt-8 mb-8" />
        <p class="font-bold text-lg mb-3">Change Password</p>
        <Form>
            <Field label="Current Password">
                <Password v-model="change_password.old_password" :fluid="true" :feedback="false" :pt="{ pcInput: { root: 'grow' } }"></Password>
            </Field>
            <Field label="New Password">
                <Password v-model="change_password.new_password" :fluid="true" :feedback="false" :pt="{ pcInput: { root: 'grow' } }"></Password>
            </Field>
            <Field label="New Password (confirm)">
                <Password v-model="change_password.new_password_confirm" :fluid="true" :feedback="false" :pt="{ pcInput: { root: 'grow' } }"></Password>
            </Field>
            <Button class="w-full" @click="changePassword" label="Save" :disabled="change_password.new_password === null || change_password.new_password !== change_password.new_password_confirm"></Button>
        </Form>
    </UserSettingsPageLayout>
</template>
