<script>
import { Card } from '@/components/card';
import DefaultSkeleton from "@/components/skeleton/DefaultSkeleton.vue";

export default {
    name: 'TopSubmitterDashboard',
    components: {DefaultSkeleton, Card },
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
                .get(this.$api.e.aStatTopSubmitters)
                .then((response) => {
                    response.data.forEach((item) => {
                        this.data.push({
                            name: item['user__username'],
                            total: item['count']
                        })
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
    <Card class="mb-3" title="Top Submitters">
        <div class="flex justify-center">
            <DefaultSkeleton v-if="loading === true"></DefaultSkeleton>
            <ul v-else class="w-full">
                <li v-for="item in data" :key="item.name" class="border rounded p-3 flex w-full">
                    <span class="flex justify-start flex-1">
                        {{ item.name }}
                    </span>
                    <span class="flex justify-end">
                        {{ item.total }} Submissions
                    </span>
                </li>
            </ul>
        </div>
    </Card>
</template>
