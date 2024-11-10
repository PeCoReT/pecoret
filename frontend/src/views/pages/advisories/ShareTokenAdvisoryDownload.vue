<script>
import AuthLayout from '@/layout/AuthLayout.vue';
import forceFileDownload from '@/utils/file';

export default {
    name: 'ShareTokenAdvisoryDownload',
    components: { AuthLayout },
    data() {
        return {
            loading: false,
            advisoryId: this.$route.params.advisoryId,
            token: this.$route.params.token,
        };
    },
    methods: {
        download() {
            this.loading = true;
            this.$api
                .get(
                    this.$api.e.aDownloadWithToken,
                    {
                        aPk: this.advisoryId,
                        token: this.token
                    },
                    null,
                    { responseType: 'arraybuffer' }
                )
                .then((resp) => {
                    forceFileDownload(resp);
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <AuthLayout title="" welcomeText="Download your Advisory!">
        <div class="grid p-fluid mt-3">
            <Button icon="fa fa-download" size="large" label="Download" :loading="loading" @click="download"></Button>
        </div>
    </AuthLayout>
</template>
