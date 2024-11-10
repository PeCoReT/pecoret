<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import ScanStatusBadge from '@/components/dialogs/attack_surface/ScanStatusBadge.vue';

export default {
    name: 'ScanDetail',
    components: { ScanStatusBadge, BaseLayout },
    data() {
        return {
            loading: false,
            scanId: this.$route.params.scanId,
            scan: { scan_type: {}, scan_types: [] },
            breadcrumbs: [
                {
                    label: 'Scans',
                    to: this.$router.resolve({
                        name: 'AttackSurfaceScanList'
                    })
                },
                {
                    label: 'Scan Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getItem();
    },
    methods: {
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this scan?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.asScanDetail, { pk: this.scanId }).then(() => {
                        this.$router.push({
                            name: 'AttackSurfaceScanList'
                        });
                    });
                }
            });
        },
        getItem() {
            this.loading = true;
            this.$api
                .get(this.$api.e.asScanDetail, { pk: this.scanId })
                .then((response) => {
                    this.scan = response.data;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <template #pre-content-right>
            <div class="flex justify-end">
                <Button icon="fa fa-trash" severity="danger" label="Delete" outlined @click="confirmDialogDelete"></Button>
            </div>
        </template>
        <div class="col-span-12" v-if="loading === false">
            <div class="card p-8">
                <!-- Scan Overview Section -->
                <div class="bg-surface-950 rounded-lg shadow-lg p-6 mb-6">
                    <div class="flex justify-between items-center mb-4">
                        <div>
                            <h2 class="text-2xl font-semibold">{{ scan.name }}</h2>
                            <p class="text-sm text-gray-400">Scan ID: {{ scan.pk }}</p>
                            <p class="text-sm text-gray-400">Started at: {{ scan.started_at || 'Not yet started!' }}</p>
                            <p class="text-sm text-gray-400" v-if="scan.finished_at">Finished at: {{ scan.finished_at }}</p>
                        </div>
                        <ScanStatusBadge :status="scan.status"></ScanStatusBadge>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h3 class="text-lg font-semibold mb-2">Scan Type</h3>
                            <p class="text-gray-300">{{ scan.scan_type.name }}</p>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold mb-2">Current Status</h3>
                            <p class="text-gray-300">{{ scan.status }}</p>
                        </div>
                    </div>
                </div>

                <div class="bg-surface-950 rounded-lg shadow-lg p-6 mb-6">
                    <h2 class="text-xl font-semibold mb-4">Scan Targets</h2>
                    <div class="overflow-y-auto max-h-64">
                        <ul class="list-disc list-inside space-y-2 text-gray-300">
                            <li v-for="obj in scan.scan_objects" :key="obj.pk">
                                {{ obj.content_type.charAt(0).toUpperCase() + obj.content_type.slice(1) }}:
                                {{ obj.asset.display_name }}
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Scan Results Section -->
                <div class="bg-surface-950 rounded-lg shadow-lg p-6 mb-6" v-if="scan.output">
                    <h2 class="text-xl font-semibold mb-4">Output</h2>
                    <div class="overflow-y-auto max-h-96">
                        <pre>{{ scan.output }}</pre>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-span-12" v-else>
            <div class="card p-8">
                <Skeleton class="mb-2"></Skeleton>
                <Skeleton width="10rem" class="mb-2"></Skeleton>
                <Skeleton width="5rem" class="mb-2"></Skeleton>
                <Skeleton height="2rem" class="mb-2"></Skeleton>
                <Skeleton width="10rem" height="4rem"></Skeleton>
            </div>
        </div>
    </BaseLayout>
</template>
