<script>
import { defineComponent } from 'vue';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { DonutChart } from '@/components/ui/chart-donut';

export default defineComponent({
    name: 'DashboardSeverityChart',
    components: { DefaultSkeleton, DonutChart },
    data() {
        return {
            loading: false,
            projectId: this.$route.params.projectId,
            options: {
                cutout: '60%'
            },
            data: [
                {
                    name: 'Critical',
                    total: 1,
                    predicted: 2
                },
                {
                    name: 'High',
                    total:3,
                    predicted: 4
                },
                {
                    name: 'Medium',
                    total: 22,
                    predicted: 11
                },
                {
                    name: 'Low',
                    total: 5,
                    predicted: 5,
                },
                {
                    name: 'Informational',
                    total: 13,
                    predicted: 13
                },
            ],
        };
    },
    mounted() {
        this.getChartData();
    },
    methods: {
        valueFormatter(tick) {
            return tick
        },
        getChartData() {
            this.loading = true;
            this.$api
                .get(this.$api.e.projectsStatusFindingDashboard, { pk: this.projectId })
                .then((response) => {
                    for(let i = 0; i<=this.data.length-1;i++) {
                        this.data[i].total = response.data[this.data[i].name];
                        this.data[i].predicted = response.data[this.data[i].name];
                    }

                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
});
</script>

<template>
    <Card title="Severities">
        <div class="flex justify-center">
            <DefaultSkeleton v-if="loading"></DefaultSkeleton>
            <DonutChart v-else index="name" :category="'total'" :data="data" :value-formatter="valueFormatter" :colors="['#8f0d2d', '#e21538', '#f0801d', '#fab725', '#86cbce']" />
        </div>
    </Card>
</template>

<style scoped></style>
