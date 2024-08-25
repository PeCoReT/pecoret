<script>
import AdvisoryService from '@/service/AdvisoryService';

export default {
    name: 'TopSubmitterDashboard',
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
            chartColors: ['--p-emerald-300', '--p-orange-300', '--p-red-300', '--p-lime-300', '--p-teal-300', '--p-green-300'],
            chartHoverColors: ['--p-emerald-200', '--p-orange-200', '--p-red-200', '--p-lime-200', '--p-teal-200', '--p-green-200'],
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    },
                    x: {
                        barPercentage: 0.4
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            },
            chartData: {
                labels: [],
                datasets: [
                    {
                        label: 'Submissions',
                        data: [],
                        borderWidth: 1,
                        barPercentage: 0.2,
                        backgroundColor: [],
                        hoverBackgroundColor: []
                    }
                ]
            }
        };
    },
    mounted() {
        this.getData();
    },
    methods: {
        getData() {
            this.loading = true;
            const documentStyle = getComputedStyle(document.body);
            this.service
                .getTopSubmittersStatistic()
                .then((response) => {
                    response.data.forEach((item) => {
                        this.chartData.labels.push(item['user__username']);
                        this.chartData.datasets[0].data.push(item['count']);
                    });
                    for (let i = 0; i < this.chartColors.length; i++) {
                        this.chartData.datasets[0].backgroundColor.push(documentStyle.getPropertyValue(this.chartColors[i]));
                        this.chartData.datasets[0].hoverBackgroundColor.push(documentStyle.getPropertyValue(this.chartHoverColors[i]));
                    }
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>
<template>
    <Card class="card mb-3">
        <template #title>Top Submitters</template>
        <template #content>
            <div class="flex justify-center">
                <Skeleton v-if="loading === true"></Skeleton>
                <Chart type="bar" :data="chartData" :options="options" class="w-full" v-else></Chart>
            </div>
        </template>
    </Card>
</template>
