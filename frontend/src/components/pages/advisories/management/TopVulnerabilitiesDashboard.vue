<script>
import AdvisoryService from "@/service/AdvisoryService";

export default {
    name: "TopVulnerabilitiesDashboard",
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
            options: {
                indexAxis: "y",
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
                        label: "Submissions",
                        data: [],
                        borderWidth: 1,
                        backgroundColor: [
                            "rgba(255, 99, 132, 0.2)",
                            "rgba(255, 159, 64, 0.2)",
                            "rgba(255, 205, 86, 0.2)",
                            "rgba(75, 192, 192, 0.2)",
                            "rgba(54, 162, 235, 0.2)",
                            "rgba(153, 102, 255, 0.2)",
                            "rgba(201, 203, 207, 0.2)"
                        ]
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
            this.service.getTopVulnerabilities(this.$api).then((response) => {
                response.data.forEach((item) => {
                    this.chartData.labels.push(item["vulnerability__name"]);
                    this.chartData.datasets[0].data.push(item["count"]);

                });
            }).finally(() => {
                this.loading = false;
            });
        }
    }
};
</script>
<template>
    <Card class="card mb-3">
        <template #title>Top Vulnerabilities</template>
        <template #content>
            <div class="flex justify-content-center">
                <Skeleton v-if="loading"></Skeleton>
                <Chart type="bar" :data="chartData" :options="options"
                       class="w-full mx-w-25rem" v-else></Chart>
            </div>
        </template>
    </Card>
</template>