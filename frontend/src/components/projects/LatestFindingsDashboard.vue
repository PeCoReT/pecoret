<script>

export default {
    name: 'LatestFindingsDashboard',
    props: {
        projectId: {
            required: true
        }
    },
    data() {
        return {
            findings: null,
        };
    },
    mounted() {
      this.getData()
    },
    methods: {
        getData() {
            let params = {
                limit: 5,
                page: 1,
                ordering: '-date_created'
            };
            this.$api.get(this.$api.e.pFindingList, {pPk: this.projectId}, params).then((response) => {
                this.findings = response.data.results;
            });
        },
        onLatestFindingVisit(pk) {
            this.$router.push({
                name: 'FindingDetail',
                params: {
                    projectId: this.projectId,
                    findingId: pk
                }
            });
        }
    }
};
</script>

<template>
    <Card class="card">
        <template #title>Latest Findings</template>
        <template #content>
            <DataView :value="findings">
                <template #list="slotProps">
                    <div class="col-span-12 rounded border border-surface-700 p-1 hover:bg-surface-950 card m-0" @click="onLatestFindingVisit(item.pk)" v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex p-4 gap-4">
                            <div class="flex justify-start w-full">
                                {{ item.vulnerability.name }} /
                                {{ item.name }}
                            </div>

                            <div class="flex items-center justify-end">
                                <span class="severity-badge" :class="'severity-' + item.severity.toLowerCase()">{{ item.severity }}</span>
                            </div>
                        </div>
                    </div>
                </template>
            </DataView>
        </template>
    </Card>
</template>
