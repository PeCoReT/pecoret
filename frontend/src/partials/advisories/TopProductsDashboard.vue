<script>
import { Card } from '@/components/card';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { BarChart } from '@/components/ui/chart-bar';

export default {
    name: 'TopProductsDashboard',
    components: { DefaultSkeleton, Card, BarChart },
    data() {
        return {
            data: [],
            loading: false
        };
    },
    mounted() {
        this.getData();
    },
    methods: {
        getData() {
            this.loading = true;
            this.$api
                .get(this.$api.e.aStatTopProducts)
                .then((response) => {
                    response.data.forEach((item) => {
                        let name = item['technology__name'];
                        if (item['technology__vendor']) {
                            name = `${item['technology__name']} (by ${item['technology__vendor']})`;
                        }
                        this.data.push({
                            name: name,
                            total: item['count']
                        });
                    });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>
<template>
    <Card title="Top Products">
        <div class="flex justify-content-center">
            <DefaultSkeleton v-if="loading"></DefaultSkeleton>
            <BarChart v-else
                index="name"
                :show-grid-line="false"
                type="grouped"
                :categories="['total']"
                :show-legend="false"
                :data="data"
                :y-formatter="
                    (tick, i) => {
                        if (Number.isInteger(tick)) {
                            return tick.toString();
                        }
                        return '';
                    }
                "
                :x-formatter="
                    (tick, i) => {
                        if (Number.isInteger(tick) && data[tick]) {
                            return data[tick]['name'];
                        }
                        return '';
                    }
                "
            ></BarChart>
        </div>
    </Card>
</template>
