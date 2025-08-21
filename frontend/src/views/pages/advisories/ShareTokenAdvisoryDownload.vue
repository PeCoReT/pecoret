<script>
import AuthLayout from '@/layout/AuthLayout.vue';
import forceFileDownload from '@/utils/file';
import { Button } from '@/components/ui/button';
import { ReloadIcon } from '@radix-icons/vue';

export default {
    name: 'ShareTokenAdvisoryDownload',
    components: { AuthLayout, Button, ReloadIcon },
    data() {
        return {
            loading: false,
            advisoryId: this.$route.params.advisoryId,
            token: this.$route.params.token
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
        <div class="grid mt-3">
            <Button :disabled="loading" icon="fa fa-download" label="Download" @click="download">
                <ReloadIcon class="w-4 h-4 mr-2 animate-spin" v-if="loading" />
                <i class="fa fa-download" v-else></i>
                Download
            </Button>
        </div>
    </AuthLayout>
</template>
