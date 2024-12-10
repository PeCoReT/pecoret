<script>

export default {
    name: 'LatestSubmissionsDashboard',
    data() {
        return {
            items: [],
            loading: false,
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                ordering: '-date_created',
                limit: 5
            };
            this.$api
                .get(this.$api.e.advisoryList, null, params)
                .then((response) => {
                    this.items = response.data.results.slice(0, 5);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getLink(pk) {
            return this.$router.resolve({
                name: 'AdvisoryDetail',
                params: {
                    advisoryId: pk
                }
            }).href;
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
                        <div class="col-span-12 rounded border border-surface-700 p-1 hover:bg-surface-950 card m-0">
                            <div class="flex p-4 gap-4">
                                <a :href="getLink(item.pk)" class="flex justify-start w-full">
                                    {{ item.title }}
                                </a>

                                <div class="flex align-center justify-end">
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
