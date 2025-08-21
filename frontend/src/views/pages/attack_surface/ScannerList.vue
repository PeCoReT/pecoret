<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { PageHeader } from '@/components/typography';

export default {
    name: 'ScannerList',
    components: { ContainerLayout, DataViewListLayout, PageHeader },
    data() {
        return {
            items: [],
            filters: {
                ordering: { value: '-last_seen' }
            }
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.$api.get(this.$api.e.asScannerList).then((response) => {
                this.items = response.data.results;
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <PageHeader>Scanners</PageHeader>
        </template>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div class="card" v-for="item in items" :key="item.pk">
                <h2 class="text-base font-semibold mb-2">{{ item.name }}</h2>
                <p><strong>Last Seen:</strong> {{ item.last_seen || 'Never' }}</p>
            </div>
        </div>
    </ContainerLayout>
</template>
