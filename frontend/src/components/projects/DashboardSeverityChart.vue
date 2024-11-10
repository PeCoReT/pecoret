<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'DashboardSeverityChart',
    data() {
        return {
            loading: false,
            projectId: this.$route.params.projectId,
            options: {
                cutout: '60%'
            },
            chartData: {
                labels: ['Critical', 'High', 'Medium', 'Low', 'Informational'],
                datasets: [
                    {
                        data: [],
                        backgroundColor: ['#8f0d2d', '#e21538', '#f0801d', '#fab725', '#86cbce']
                    }
                ]
            }
        };
    },
    mounted() {
        this.getChartData();
    },
    methods: {
        getChartData() {
            this.loading = true;
            this.$api
                .get(this.$api.e.projectsStatusFindingDashboard, { pk: this.projectId })
                .then((response) => {
                    this.chartData.datasets[0].data = [response.data.Critical, response.data.High, response.data.Medium, response.data.Low, response.data.Informational];
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
});
</script>

<template>
    <Card class="card">
        <template #title>Severities</template>
        <template #content>
            <div class="flex justify-center">
                <Skeleton v-if="loading"></Skeleton>
                <Chart type="doughnut" :data="chartData" :options="options" class="w-full max-w-[25rem]"></Chart>
            </div>
        </template>
    </Card>
</template>

<style scoped></style>
