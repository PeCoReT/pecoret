<script>
import { Tabs } from '@/components/tabs';

export default {
    name: 'AdvisoryTabMenu',
    components: { Tabs },
    data() {
        return {
            items: [
                {
                    label: 'Details',
                    route: this.$router.resolve({
                        name: 'AdvisoryDetail',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    }).href
                },
                {
                    label: 'Timeline',
                    route: this.$router.resolve({
                        name: 'AdvisoryTimelineList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    }).href
                },
                {
                    label: 'Comments',
                    route: this.$router.resolve({
                        name: 'AdvisoryCommentList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    }).href
                },
                {
                    label: 'Share Tokens',
                    route: this.$router.resolve({
                        name: 'AdvisoryShareTokenList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    }).href
                }
            ]
        };
    }
};
</script>

<template>
    <Tabs :items="items" class="md:max-w-lg"></Tabs>
</template>
