<script>
import AuthLayout from '@/layout/AuthLayout.vue';
import forceFileDownload from "@/utils/file";
import AdvisoryService from "@/service/AdvisoryService";

export default {
    name: 'ShareTokenAdvisoryDownload',
    components: { AuthLayout },
    data() {
        return {
            loading: false,
            advisoryId: this.$route.params.advisoryId,
            token: this.$route.params.token,
            service: new AdvisoryService()
        }
    },
    methods: {
        download() {
            this.loading = true
            this.service.downloadAdvisoryWithShareToken(this.advisoryId, this.token).then((resp) => {
                forceFileDownload(resp)
            }).finally(() => {
                this.loading = false
            })
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
