<script>
import { listViewMixin } from '@/mixins/listViewMixin';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import ScanStatusBadge from '@/partials/attack_surface/ScanStatusBadge.vue';
import { Paginator } from '@/components/paginator';
import {Button} from '@/components/ui/button';

export default {
    name: 'ScanTaskDetailList',
    components: { Paginator, ScanStatusBadge, DataViewHeader, DataViewContent, Button },
    mixins: [listViewMixin],
    data() {
        return {
            loading: false,
            scanId: this.$route.params.scanId,
            items: [],
            filters: {
                ordering: { value: '-date_updated' },
                scan: { value: this.$route.params.scanId }
            }
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asScanTaskList, {}, data)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <DataViewHeader :total-records="totalRecords">
    </DataViewHeader>
    <DataViewContent v-model:items="items" :loading="loading">
        <template #item="{ item }">
            <div class="flex-1">
                <a :href="this.$router.resolve({ name: 'AttackSurfaceScanTaskDetail', params: { taskId: item.pk } }).href" class="hover:underline">
                    [{{item.program.name }}] {{ item.pk }}

                </a>
                <div class="flex text-xs text-muted-foreground">
                    <span>
                        Created: <span>{{ item.date_created }}</span>
                    </span>
                    <span class="mx-2">|</span>
                    <span> Updated: {{ item.date_updated }} </span>
                </div>
            </div>
            <div>
                <ScanStatusBadge :status="item.status"></ScanStatusBadge>
            </div>
        </template>
    </DataViewContent>
    <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
</template>
