<script>
import AdvisoryService from '@/service/AdvisoryService';

export default {
    name: 'LatestSubmissionsDashboard',
    data() {
        return {
            items: [],
            loading: false,
            service: new AdvisoryService()
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                ordering: '-date_created'
            };
            this.service
                .getInbox(this.$api, params)
                .then((response) => {
                    this.items = response.data.results.slice(0, 5);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onLatestVisit(pk) {
            this.$router.push({
                name: 'AdvisoryDetail',
                params: {
                    advisoryId: pk
                }
            });
        }
    }
};
</script>

<template>
    <Card class="card">
        <template #title>Latest Submissions</template>
        <template #content>
            <DataView :value="items" v-if="loading === false">
                <template #list="slotProps">
                    <div v-for="(item, index) in slotProps.items" :key="index">
                        <div class="col-12 border-round border-1 hover:surface-hover" @click="onLatestVisit(item.pk)">
                            <div class="flex p-4 gap-4">
                                <div class="flex justify-content-start w-full">
                                    {{ item.vulnerability.name }} / {{ item.internal_name }} in
                                    {{ item.product }}
                                </div>

                                <div class="flex align-items-center justify-content-end">
                                    <span class="severity-badge" :class="'severity-' + item.severity.toLowerCase()">{{ item.severity }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </DataView>
            <Skeleton v-else></Skeleton>
        </template>
    </Card>
</template>

<style scoped></style>