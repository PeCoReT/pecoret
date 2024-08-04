<script>
import AdvisoryService from '@/service/AdvisoryService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import TopSubmitterDashboard from '@/components/advisories/TopSubmitterDashboard.vue';
import TopVulnerabilitiesDashboard from '@/components/advisories/TopVulnerabilitiesDashboard.vue';
import TopProductsDashboard from '@/components/advisories/TopProductsDashboard.vue';
import TopVendorsDashboard from '@/components/advisories/TopVendorsDashboard.vue';
import LatestSubmissionsDashboard from '@/components/advisories/LatestSubmissionsDashboard.vue';
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
            service: new AdvisoryService()
        };
    },
    mounted() {
        this.getStatistics();
    },
    methods: {
        getStatistics() {
            this.service.getBaseInformationStatistics(this.$api).then((response) => {
                this.statistics = response.data;
            });
        }
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <div class="col-12 md:col-6 lg:col-6 xl:col-3">
            <DetailCardWithIcon title="Inbox" :text="statistics.inbox_count" icon="fa fa-inbox"></DetailCardWithIcon>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-3">
            <DetailCardWithIcon title="Unfixed" :text="statistics.inbox_unfixed_count" icon="fa fa-bookmark"></DetailCardWithIcon>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-3">
            <DetailCardWithIcon title="Fixed" :text="statistics.inbox_fixed_count" icon="fa fa-check"></DetailCardWithIcon>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-3">
            <DetailCardWithIcon title="Won't Fix" :text="statistics.inbox_wontfix_count" icon="fa fa-clipboard-question"></DetailCardWithIcon>
        </div>
    </BaseLayout>

    <div class="grid">
        <div class="col-12 md:col-6 lg:col-6 xl:col-4">
            <TopSubmitterDashboard></TopSubmitterDashboard>

            <div class="mt-3">
                <TopVendorsDashboard></TopVendorsDashboard>
            </div>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-4">
            <TopVulnerabilitiesDashboard></TopVulnerabilitiesDashboard>
            <div class="mt-3">
                <LatestSubmissionsDashboard></LatestSubmissionsDashboard>
            </div>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-4">
            <DetailCardWithIcon title="Next Disclosure" :text="statistics.inbox_next_disclosure_date" style-class="" icon="fa fa-clock"></DetailCardWithIcon>

            <div class="mt-3">
                <TopProductsDashboard></TopProductsDashboard>
            </div>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-4"></div>
    </div>
</template>
