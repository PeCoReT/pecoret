<script>
import AdvisoryService from '@/service/AdvisoryService';

export default {
    name: 'TopProductsDashboard',
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
            chartColors: ['--orange-300', '--red-300', '--purge-300', '--teal-300', '--green-300', '--cyan-300'],
            chartHoverColors: ['--orange-200', '--red-200', '--purge-200', '--teal-200', '--green-200', '--cyan-200'],
            options: {
                scales: {
                    y: {
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
                        label: 'Products',
                        data: [],
                        borderWidth: 1,
                        barPercentage: 0.2,
                        hoverBackgroundColor: [],
                        backgroundColor: []
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
                .getTopProductsStatistics(this.$api)
                .then((response) => {
                    response.data.forEach((item) => {
                        let name = item['technology__name'];
                        if (item['technology__vendor']) {
                            name = `${item['technology__name']} (by ${item['technology__vendor']})`;
                        }
                        this.chartData.labels.push(name);
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
    <Card class="card">
        <template #title>Top Products</template>
        <template #content>
            <div class="flex justify-content-center">
                <Skeleton v-if="loading"></Skeleton>
                <Chart type="bar" :data="chartData" :options="options" class="w-full mx-w-25rem" v-else></Chart>
            </div>
        </template>
    </Card>
</template>
