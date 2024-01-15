<script>
import AdvisoryService from '@/service/AdvisoryService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import TopSubmitterDashboard from '@/components/pages/advisories/management/TopSubmitterDashboard.vue';
import TopVulnerabilitiesDashboard from '@/components/pages/advisories/management/TopVulnerabilitiesDashboard.vue';
import TopProductsDashboard from '@/components/pages/advisories/management/TopProductsDashboard.vue';
import TopVendorsDashboard from '@/components/pages/advisories/management/TopVendorsDashboard.vue';
import LatestSubmissionsDashboard from '@/components/pages/advisories/management/LatestSubmissionsDashboard.vue';

export default {
    name: 'AdvisoryManagementDashboard',
    components: {
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
            this.service.getInboxStatistics(this.$api).then((response) => {
                this.statistics = response.data;
            });
        }
    }
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
            <div class="flex justify-content-end"></div>
        </div>
    </div>

    <div class="grid">
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
    </div>

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
            <Card class="card mb-3">
                <template #title>Quick Links</template>
                <template #content>
                    <Button @click="this.$router.push(this.$router.resolve({ name: 'AdvisoryInbox' }))" outlined>Inbox </Button>
                </template>
            </Card>
            <DetailCardWithIcon title="Next Disclosure" :text="statistics.inbox_next_disclosure_date" style-class="" icon="fa fa-clock"></DetailCardWithIcon>

            <div class="mt-3">
                <TopProductsDashboard></TopProductsDashboard>
            </div>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-4"></div>
    </div>
</template>