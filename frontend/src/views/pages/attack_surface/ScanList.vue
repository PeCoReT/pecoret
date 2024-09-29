<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import { useListViewComposable } from '@/composables/listViewComposable';
import ScanStatusBadge from '@/components/dialogs/attack_surface/ScanStatusBadge.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import ScanCreateDialog from '@/components/dialogs/attack_surface/ScanCreateDialog.vue';

export default {
    name: 'ASScanList.vue',
    components: { ScanCreateDialog, BlankSlate, ScanStatusBadge, BaseListLayout },
    data() {
        return {
            service: new ASMonitorService(),
            breadcrumbs: [
                {
                    label: 'Scans',
                    disabled: true
                }
            ],
            search: null,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            filters: {},
            token: null,
            listComposable: useListViewComposable()
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.service
                .getScans(data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onSearch(value) {
            this.getItems({ search: value });
        }
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #head-left>
            <InputText placeholder="Search" @update:modelValue="onSearch" v-model="search"></InputText>
        </template>
        <template #create-button>
            <ScanCreateDialog @object-created="getItems"></ScanCreateDialog>
        </template>
        <div class="card text-gray-100 p-8">
            <h1 class="text-3xl font-semibold mb-8">Scans Overview</h1>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" v-if="loading === false">
                <div class="bg-surface-950 rounded-lg shadow-lg p-6 flex flex-col h-72" v-for="scan in items" :key="scan.pk">
                    <div class="flex justify-between items-center mb-4">
                        <div>
                            <h2 class="text-xl font-semibold">{{ scan.name }} / {{ scan.scan_type.name }}</h2>
                            <p class="text-sm text-gray-400">Scan ID: {{ scan.pk }}</p>
                        </div>
                        <ScanStatusBadge :status="scan.status"></ScanStatusBadge>
                    </div>

                    <div class="mb-4 flex-1 overflow-y-auto">
                        <h3 class="text-lg font-semibold mb-2">Targets</h3>
                        <ul class="list-disc list-inside space-y-1">
                            <li v-for="obj in scan.scan_objects.slice(0, 5)" :key="obj.content_type + '-' + obj.object_id">
                                {{ obj.content_type.charAt(0).toUpperCase() + obj.content_type.slice(1) }}:
                                <span v-if="obj.asset">{{ obj.asset.display_name }}</span>
                            </li>
                        </ul>
                    </div>

                    <div class="flex justify-end">
                        <Button @click="this.$router.push({ name: 'AttackSurfaceScanDetail', params: { scanId: scan.pk } })"> View Details </Button>
                    </div>
                </div>
                <div class="lg:col-span-3 md:grid-cols-2 grid-cols-1" v-if="items.length < 1">
                    <BlankSlate title="No Scans!" text="No scans found!" icon="fa fa-binoculars"></BlankSlate>
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" v-else>
                <Skeleton class="mb-2"></Skeleton>
                <Skeleton width="10rem" class="mb-2"></Skeleton>
                <Skeleton width="5rem" class="mb-2"></Skeleton>
                <Skeleton height="2rem" class="mb-2"></Skeleton>
                <Skeleton width="10rem" height="4rem"></Skeleton>
            </div>
        </div>
        <div class="pb-6">
            <Paginator :total-records="this.totalRecords" :rows="this.pagination.limit" @page="onPage"></Paginator>
        </div>
    </BaseListLayout>
</template>
