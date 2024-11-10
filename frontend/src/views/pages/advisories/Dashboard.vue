<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import TopSubmitterDashboard from '@/components/cards/dashboards/advisories/TopSubmitterDashboard.vue';
import TopVulnerabilitiesDashboard from '@/components/cards/dashboards/advisories/TopVulnerabilitiesDashboard.vue';
import TopProductsDashboard from '@/components/cards/dashboards/advisories/TopProductsDashboard.vue';
import TopVendorsDashboard from '@/components/cards/dashboards/advisories/TopVendorsDashboard.vue';
import LatestSubmissionsDashboard from '@/components/cards/dashboards/advisories/LatestSubmissionsDashboard.vue';
import BaseLayout from '@/layout/base/BaseLayout.vue';

export default {
    name: 'AdvisoryDashboard',
    components: {
        BaseLayout,
        LatestSubmissionsDashboard,
        TopVendorsDashboard,
        TopProductsDashboard,
        TopVulnerabilitiesDashboard,
        TopSubmitterDashboard,
        DetailCardWithIcon
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Dashboard',
                    disabled: true
                }
            ],
            statistics: {},
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
    <BaseLayout :breadcrumbs="breadcrumbs">
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-3 mt-3">
            <DetailCardWithIcon title="Inbox" :text="statistics.inbox_count" icon="fa fa-inbox"></DetailCardWithIcon>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-3 mt-3">
            <DetailCardWithIcon title="Unfixed" :text="statistics.inbox_unfixed_count" icon="fa fa-bookmark"></DetailCardWithIcon>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-3 mt-3">
            <DetailCardWithIcon title="Fixed" :text="statistics.inbox_fixed_count" icon="fa fa-check"></DetailCardWithIcon>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-3 mt-3">
            <DetailCardWithIcon title="Won't Fix" :text="statistics.inbox_wontfix_count" icon="fa fa-clipboard-question"></DetailCardWithIcon>
        </div>
    </BaseLayout>

    <div class="grid grid-cols-12 mt-3 gap-3">
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-4">
            <TopSubmitterDashboard></TopSubmitterDashboard>

            <div class="mt-3">
                <TopVendorsDashboard></TopVendorsDashboard>
            </div>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-4 gap-3">
            <TopVulnerabilitiesDashboard></TopVulnerabilitiesDashboard>
            <div class="mt-3">
                <LatestSubmissionsDashboard></LatestSubmissionsDashboard>
            </div>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-4 gap-3">
            <DetailCardWithIcon title="Next Disclosure" :text="statistics.inbox_next_disclosure_date" style-class="" icon="fa fa-clock"></DetailCardWithIcon>

            <div class="mt-3">
                <TopProductsDashboard></TopProductsDashboard>
            </div>
        </div>
        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-4 gap-3"></div>
    </div>
</template>
