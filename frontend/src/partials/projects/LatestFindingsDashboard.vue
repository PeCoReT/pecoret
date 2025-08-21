<script>
import { Badge } from '@/components/badge';
import { Card } from '@/components/card';
import DataViewContent from '@/components/dataview/DataViewContent.vue';

export default {
    name: 'LatestFindingsDashboard',
    components: { DataViewContent, Badge, Card },
    props: {
        projectId: {
            required: true
        }
    },
    data() {
        return {
            findings: [],
            loading: false
        };
    },
    mounted() {
        this.getData();
    },
    methods: {
        getData() {
            this.loading = true;
            let params = {
                limit: 5,
                page: 1,
                ordering: '-date_created'
            };
            this.$api
                .get(this.$api.e.pFindingList, { pPk: this.projectId }, params)
                .then((response) => {
                    this.findings = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getFindingUrl(pk) {
            return this.$router.resolve({
                name: 'FindingDetail',
                params: {
                    projectId: this.projectId,
                    findingId: pk
                }
            }).href;
        }
    }
};
</script>

<template>
    <Card title="Latest Findings">
        <DataViewContent :items="findings" :loading="loading" class="hover:bg-accent hover:text-accent-foreground rounded-lg">
            <template #item="{ item }">
                <div class="flex-1">
                    <div class="flex p-1 gap-4">
                        <a :href="getFindingUrl(item.pk)" class="flex justify-start w-full">
                            {{ item.vulnerability.name }} /
                            {{ item.name }}
                        </a>
                    </div>
                </div>
                <div class="flex align-center justify-end">
                    <Badge :text="item.severity" :variant="item.severity"></Badge>
                </div>
            </template>
            <template #blankslate>
                <p>No results!</p>
            </template>
        </DataViewContent>
    </Card>
</template>
