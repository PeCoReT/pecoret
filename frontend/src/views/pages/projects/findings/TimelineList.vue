<script>
import FindingTabMenu from '@/components/navigation/FindingTabMenu.vue';

export default {
    name: 'TimelineList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            items: [],
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'FindingList',
                        params: { projectId: this.$route.params.projectId }
                    })
                },
                {
                    label: 'Finding Detail',
                    to: this.$router.resolve({
                        name: 'FindingDetail',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    })
                },
                {
                    label: 'Timeline',
                    disabled: true
                }
            ]
        };
    },
    methods: {
        getTimeline() {
            this.$api
                .get(this.$api.e.pFindingTimelineList, {
                    pPk: this.projectId,
                    fPk: this.findingId
                })
                .then((response) => {
                    this.items = response.data.results;
                });
        }
    },
    mounted() {
        this.getTimeline();
    },
    components: { FindingTabMenu }
};
</script>

<template>
    <div class="grid grid-cols-1 mt-3">
        <div class="col-span-1">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid grid-cols-1 mt-3">
        <div class="col-span-1">
            <FindingTabMenu class="surface-card"></FindingTabMenu>
            <div class="card border-noround-top">
                <Timeline :value="items" class="mt-3">
                    <template #opposite="slotProps">
                        <small class="p-text-secondary">{{ slotProps.item.date_created }}</small>
                    </template>
                    <template #content="slotProps">
                        {{ slotProps.item.title }}
                    </template>
                </Timeline>
            </div>
        </div>
    </div>
</template>
