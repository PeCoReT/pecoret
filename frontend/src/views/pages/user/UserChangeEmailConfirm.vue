<script>
export default {
    name: 'UserChangeEmailConfirm',

    methods: {
        change_email_confirm() {
            let data = {
                uid: this.$route.params.uid,
                token: this.$route.params.token
            };
            this.$api
                .post(this.$api.e.userChangeEmailConfirm, data)
                .then(() => {})
                .finally(() => {
                    this.$router.push({
                        name: 'UserProfileSettings'
                    });
                });
        }
    }
};
</script>

<template>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12 md:col-span-6 md:col-start-3">
            <Card>
                <template #title>Confirm Email</template>
                <template #content>
                    <Button @click="change_email_confirm" outlined>Submit</Button>
                </template>
            </Card>
        </div>
    </div>
</template>
