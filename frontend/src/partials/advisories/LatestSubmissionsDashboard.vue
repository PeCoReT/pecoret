<script>
import { Badge } from '@/components/badge';
import { Card } from '@/components/card';
import DataViewContent from '@/components/dataview/DataViewContent.vue';

export default {
    name: 'LatestSubmissionsDashboard',
    components: { DataViewContent, Badge, Card },
    data() {
        return {
            items: [],
            loading: false
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
    <Card title="Latest Submissions">
        <DataViewContent :items="items" :loading="loading" class="!p-0 hover:bg-accent hover:text-accent-foreground !rounded-none">
            <template #item="{ item }">
                <a class="w-full p-0 m-0" :href="getLink(item.pk)">
                    <div class="flex p-4 gap-4">
                        <span class="flex justify-start w-full">
                            {{ item.title }}
                        </span>
                        <div class="flex align-center justify-end">
                            <Badge :text="item.severity" :variant="item.severity"></Badge>
                        </div>
                    </div>
                </a>
            </template>
        </DataViewContent>
    </Card>
</template>
