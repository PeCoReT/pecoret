<script>
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import PageHeader from '@/components/typography/PageHeader.vue';
import ScanStatusBadge from '@/partials/attack_surface/ScanStatusBadge.vue';
import BackLinkButton from '@/components/button/BackLinkButton.vue';
import BlankSlate from '@/components/blankslate/BlankSlate.vue';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';

export default {
    name: 'ScanTaskDetail',
    components: { DefaultSkeleton, BlankSlate, BackLinkButton, ScanStatusBadge, PageHeader, ContainerLayout },
    data() {
        return {
            taskId: this.$route.params.taskId,
            item: { scan_template: {} },
            loading: false
        };
    },
    mounted() {
        this.getItem();
    },
    methods: {
        getItem() {
            this.loading = true;
            this.$api
                .get(this.$api.e.asScanTaskDetail, { pk: this.taskId })
                .then((response) => {
                    this.item = response.data;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <BackLinkButton text="Back To Scan" :href="this.$router.resolve({ name: 'AttackSurfaceScanDetail', params: { scanId: item.scan.pk } }).href" v-if="item && item.scan"></BackLinkButton>
        <PageHeader>
            <div class="grid grid-cols-12">
                <div class="col-span-11">Scan: {{ item.pk }} ({{ item.scan_template.name }})</div>
                <div class="col-span-1">
                    <div class="flex justify-end">
                        <ScanStatusBadge :status="item.status"></ScanStatusBadge>
                    </div>
                </div>
            </div>
        </PageHeader>
        <div v-if="loading === false">
            <p><strong>Date Created: </strong> {{ item.date_created }}</p>
            <p><strong>Date Updated: </strong> {{ item.date_updated }}</p>
            <p><strong>Started At: </strong> {{ item.batch_start_time || '-' }}</p>
            <p><strong>Finished At: </strong> {{ item.batch_end_time || '-' }}</p>

            <Card class="mt-3">
                <h2 class="text-lg">Scan Items</h2>
                <ul>
                    <li v-for="t in item.targets">
                        {{ t.display_name }}
                    </li>
                    <li v-for="t in item.services">
                        {{ t.display_name }}
                    </li>
                    <li v-for="t in item.urls">
                        {{ t.display_name }}
                    </li>
                </ul>
            </Card>

            <Card class="mt-3">
                <h2 class="text-lg">Output</h2>
                <div v-if="item.raw_output" class="overflow-y-auto">
                    <pre>{{ item.raw_output }}</pre>
                </div>
                <p v-else>No Output</p>
            </Card>

            <Card class="mt-3">
                <h2 class="text-lg">Errors</h2>
                <div v-if="item.errors" class="overflow-y-auto">
                    <pre>{{ item.errors }}</pre>
                </div>
                <p v-else>No Errors</p>
            </Card>
        </div>
        <DefaultSkeleton v-else></DefaultSkeleton>
    </ContainerLayout>
</template>
