<script>
import { Card } from '@/components/card';

export default {
    name: 'UserChangeEmailConfirm',
    components: { Card },
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
            <Card title="Confirm Email">
                <Button outlined @click="change_email_confirm">Submit</Button>
            </Card>
        </div>
    </div>
</template>
