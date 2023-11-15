<script>
import FindingService from '@/service/FindingService';
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue';

export default {
    name: 'TimelineList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            findingService: new FindingService(),
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
            this.findingService.getTimeline(this.projectId, this.findingId).then((response) => {
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
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
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