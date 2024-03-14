<script>
import ASMonitorService from '@/service/ASMonitorService';

export default {
    name: 'FindingsByDatesChart',
    props: {
        programId: {
            required: true
        }
    },
    data() {
        return {
            loading: false,
            loaded: false,
            options: {
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            },
            chartData: {
                labels: [],
                datasets: [
                    {
                        data: []
                    }
                ]
            },
            service: new ASMonitorService()
        };
    },
    methods: {
        getData() {
            let labels = [];
            let data = [];
            this.service.getFindingsByDateStats(this.$api, this.programId).then((response) => {
                for (let [key, value] of Object.entries(response.data)) {
                    labels.push(key);
                    data.push(value);
                }
                this.chartData.labels = labels;
                this.chartData.datasets[0].data = data;
            });
        }
    },
    watch: {
        programId: {
            handler(value) {
                if (value && this.loaded === false) {
                    this.loaded = true;
                    this.getData();
                }
            }
        }
    }
};
</script>

<template>
    <Card class="card">
        <template #title>Findings By Date</template>
        <template #content>
            <div class="flex justify-content-center">
                <Skeleton v-if="loading"></Skeleton>
                <Chart type="line" :data="chartData" :options="options" class="w-full h-25rem flex justify-content-center" v-else></Chart>
            </div>
        </template>
    </Card>
</template>
