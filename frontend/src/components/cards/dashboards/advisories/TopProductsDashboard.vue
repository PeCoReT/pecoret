<script>

export default {
    name: 'TopProductsDashboard',
    data() {
        return {
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
            this.$api
                .get(this.$api.e.aStatTopProducts)
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
