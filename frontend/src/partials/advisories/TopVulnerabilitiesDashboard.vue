<script>
import { Card } from '@/components/card';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { BarChart } from '@/components/ui/chart-bar';

export default {
    name: 'TopVulnerabilitiesDashboard',
    components: { BarChart, DefaultSkeleton, Card },
    data() {
        return {
            loading: false,
            data: []
        };
    },
    mounted() {
        this.getData();
    },
    methods: {
        getData() {
            this.loading = true;
            this.$api
                .get(this.$api.e.aStatTopVulns)
                .then((response) => {
                    response.data.forEach((item) => {
                        let name = item['cwes__name'];
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
    <Card class="mb-3" title="Top Vulnerabilities">
        <div class="flex justify-center">
            <DefaultSkeleton v-if="loading"></DefaultSkeleton>
            <BarChart
                v-else
                :show-grid-line="false"
                index="name"
                :categories="['total']"
                :data="data"
                :show-legend="false"
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
