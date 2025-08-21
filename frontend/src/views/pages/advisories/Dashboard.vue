<script>
import TopProductsDashboard from '@/partials/advisories/TopProductsDashboard.vue';
import LatestSubmissionsDashboard from '@/partials/advisories/LatestSubmissionsDashboard.vue';
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { DetailCardWithIcon } from '@/components/card';
import TopVulnerabilitiesDashboard from '@/partials/advisories/TopVulnerabilitiesDashboard.vue';
import TopSubmitterDashboard from '@/partials/advisories/TopSubmitterDashboard.vue';

export default {
    name: 'AdvisoryDashboard',
    components: {
        TopSubmitterDashboard,
        TopVulnerabilitiesDashboard,
        BaseLayout,
        LatestSubmissionsDashboard,
        TopProductsDashboard,
        DetailCardWithIcon
    },
    data() {
        return {
            statistics: {}
        };
    },
    mounted() {
        this.getStatistics();
    },
    methods: {
        getStatistics() {
            this.$api.get(this.$api.e.aStatBaseInfo).then((response) => {
                this.statistics = response.data;
            });
        }
    }
};
</script>

<template>
    <BaseLayout>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-3 mt-8">
            <DetailCardWithIcon :text="statistics.inbox_count" icon="fa fa-inbox" title="Inbox"></DetailCardWithIcon>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-3 mt-8">
            <DetailCardWithIcon :text="statistics.inbox_unfixed_count" icon="fa fa-bookmark" title="Unfixed"></DetailCardWithIcon>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-3 mt-8">
            <DetailCardWithIcon :text="statistics.inbox_fixed_count" icon="fa fa-check" title="Fixed"></DetailCardWithIcon>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-3 mt-8">
            <DetailCardWithIcon :text="statistics.inbox_disclosed_count" icon="fa fa-bullhorn" title="Disclosed"></DetailCardWithIcon>
        </div>
    </BaseLayout>

    <div class="grid grid-cols-12 mt-3 gap-3">
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-4">
            <TopSubmitterDashboard></TopSubmitterDashboard>
            <LatestSubmissionsDashboard></LatestSubmissionsDashboard>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-4 gap-3">
            <TopVulnerabilitiesDashboard></TopVulnerabilitiesDashboard>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-4 gap-3">
            <DetailCardWithIcon :text="statistics.inbox_next_disclosure_date" icon="fa fa-clock" style-class="" title="Next Disclosure"></DetailCardWithIcon>

            <div class="mt-3">
                <TopProductsDashboard></TopProductsDashboard>
            </div>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-4 gap-3"></div>
    </div>
</template>
