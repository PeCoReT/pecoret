<script>
import UserSettingsPageLayout from '@/layout/UserSettingsPageLayout.vue';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

export default {
    name: 'UserProfileSettings',
    components: { UserSettingsPageLayout, Input, Button },
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
                        });
                    }
                },
                {
                    label: 'Notifications',
                    command: () => {
                        this.$router.push({
                            name: 'UserSettingsDetail'
                        });
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
                this.$toaster({
                    title: 'Updated',
                    description: 'Settings were updated successfully!',
                    duration: 3000
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
                this.$toaster({
                    title: 'Password changed',
                    duration: 3000,
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
                this.$toaster({
                    title: 'Change Email',
                    duration: 3000,
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
    <UserSettingsPageLayout headline="Account" subheadline="Update your personal data here!">
        <p class="font-bold text-lg mb-3">Profile</p>
        <Form>
            <Field label="First Name">
                <Input v-model="model.first_name"></Input>
            </Field>
            <Field label="Last Name">
                <Input v-model="model.last_name"></Input>
            </Field>
            <Field label="Nickname">
                <Input v-model="model.nickname"></Input>
            </Field>
            <Button class="w-full" @click="patch">Save</Button>
        </Form>
        <hr class="mt-8 mb-8" />

        <p class="font-bold text-lg mb-3">Change E-Mail</p>
        <Form>
            <Field label="Password">
                <Input v-model="new_email.password" type="password"></Input>
            </Field>
            <Field label="New Email">
                <Input id="new_user-help" v-model="new_email.mail" type="email"></Input>
                <small id="new_user-help">Current: {{ this.model.email }}.</small>
            </Field>
            <Button class="w-full" @click="changeEmail">Save</Button>
        </Form>

        <hr class="mt-8 mb-8" />
        <p class="font-bold text-lg mb-3">Change Password</p>
        <Form>
            <Field label="Current Password">
                <Input v-model="change_password.old_password" type="password"></Input>
            </Field>
            <Field label="New Password">
                <Input v-model="change_password.new_password" type="password"></Input>
            </Field>
            <Field label="New Password (confirm)">
                <Input v-model="change_password.new_password_confirm" type="password"></Input>
            </Field>
            <Button :disabled="change_password.new_password === null || change_password.new_password !== change_password.new_password_confirm" class="w-full" @click="changePassword"> Save </Button>
        </Form>
    </UserSettingsPageLayout>
</template>
