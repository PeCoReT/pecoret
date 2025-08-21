<script>
import { Tabs } from '@/components/tabs';

export default {
    name: 'FindingTabMenu',
    components: { Tabs },
    data() {
        return {
            items: [
                {
                    label: 'Details',
                    route: this.$router.resolve({
                        name: 'FindingDetail',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    }).href
                },
                {
                    label: 'Comments',
                    route: this.$router.resolve({
                        name: 'FindingCommentList',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    }).href
                },
                {
                    label: 'Timeline',
                    route: this.$router.resolve({
                        name: 'FindingTimelineList',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    }).href
                },
                {
                    label: 'Scores',
                    route: this.$router.resolve({
                        name: 'FindingScoreList',
                        params: {
                            projectId: this.$route.params.projectId,
                            findingId: this.$route.params.findingId
                        }
                    }).href
                },
                {
                    label: 'Retest',
                    route: this.$router.resolve({
                        name: 'FindingRetest',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    }).href
                }
            ]
        };
    }
};
</script>

<template>
    <Tabs :items="items"></Tabs>
</template>
