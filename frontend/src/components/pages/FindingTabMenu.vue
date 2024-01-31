<script>
export default {
    name: 'FindingTabMenu',
    mounted() {
        this.activeItem = this.items.findIndex((item) => this.$route.path === this.$router.resolve(item.route).path);
    },
    data() {
        return {
            activeItem: null,
            items: [
                {
                    label: 'Details',
                    route: this.$router.resolve({
                        name: 'FindingDetail',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    })
                },
                {
                    label: 'Comments',
                    route: this.$router.resolve({
                        name: 'FindingCommentList',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    })
                },
                {
                    label: 'Timeline',
                    route: this.$router.resolve({
                        name: 'FindingTimelineList',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    })
                },
                {
                    label: 'Scores',
                    route: this.$router.resolve({
                        name: 'FindingScoreList',
                        params: {
                            projectId: this.$route.params.projectId,
                            findingId: this.$route.params.findingId
                        }
                    })
                },
                {
                    label: 'Retest',
                    route: this.$router.resolve({
                        name: 'FindingRetest',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
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
