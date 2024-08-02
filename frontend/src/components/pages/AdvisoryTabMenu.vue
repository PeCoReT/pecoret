<script>
export default {
    name: 'AdvisoryTabMenu',
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
                    })
                },
                {
                    label: 'Proofs',
                    route: this.$router.resolve({
                        name: 'AdvisoryProofList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Timeline',
                    route: this.$router.resolve({
                        name: 'AdvisoryTimelineList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Comments',
                    route: this.$router.resolve({
                        name: 'AdvisoryCommentList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                }
            ]
        };
    }
};
</script>

<template>
    <pTabMenu v-model="items"></pTabMenu>
</template>