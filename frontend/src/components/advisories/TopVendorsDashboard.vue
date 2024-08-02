<script>
import AdvisoryService from '@/service/AdvisoryService';

export default {
    name: 'TopVendorsDashboard',
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
            chartColors: ['--purple-300', '--teal-300', '--red-300', '--green-300', '--cyan-300', '--orange-300'],
            chartHoverColors: ['--purple-200', '--teal-200', '--red-200', '--green-200', '--cyan-200', '--orange-200'],
            options: {
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
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
            this.service
                .getTopVendorsStatistics(this.$api)
                .then((response) => {
                    response.data.forEach((item) => {
                        this.chartData.labels.push(item['technology__vendor']);
                        this.chartData.datasets[0].data.push(item['count']);
                    });
                    const documentStyle = getComputedStyle(document.body);
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
    <Card class="card">
        <template #title>Top Vendors</template>
        <template #content>
            <div class="flex justify-content-center">
                <Skeleton v-if="loading"></Skeleton>
                <Chart type="bar" :data="chartData" :options="options" class="w-full mx-w-25rem" v-else></Chart>
            </div>
        </template>
    </Card>
</template>
