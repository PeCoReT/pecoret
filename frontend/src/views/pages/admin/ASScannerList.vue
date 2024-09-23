<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import { useListViewComposable } from '@/composables/listViewComposable';
import ScannerCreateDialog from '@/components/dialogs/attack_surface/admin/ScannerCreateDialog.vue';
import ScannerUpdateDialog from '@/components/dialogs/attack_surface/admin/ScannerUpdateDialog.vue';

export default {
    name: 'ASScannerList.vue',
    components: { ScannerUpdateDialog, ScannerCreateDialog, GenericDataTable, BaseListLayout },
    data() {
        return {
            service: new ASMonitorService(),
            breadcrumbs: [
                {
                    label: 'Scanners',
                    disabled: true
                }
            ],
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
                .getScanners(data)
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
        onSearch(query) {
            this.getItems({ search: query });
        },
        onCreated(data) {
            this.token = data.token;
            this.getItems();
        },
        getScanTypeDisplay(item) {
            let names = [];
            if (item.scan_types && item.scan_types.length > 0) {
                item.scan_types.forEach((item) => {
                    names.push(item.name);
                });
            }
            if (names.length < 1) {
                return '-';
            }
            return names.join(',');
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this scanner?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteScanner(id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Scanner was removed!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ScannerCreateDialog @object-created="onCreated"></ScannerCreateDialog>
        </template>
        <template #table>
            <div v-if="token" class="bg-gray-400 text-gray-800 p-3 rounded">Scanner Token: {{ token }}</div>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No scanners found!"
                blank-slate-title="No Scanners!"
                blank-slate-icon="fa fa-binoculars"
                :model-value="items"
                @page="onPage"
                @search="onSearch"
                :show-search="true"
            >
                <Column header="Name" field="name"></Column>
                <Column header="Scan Types">
                    <template #body="slotProps">
                        {{ getScanTypeDisplay(slotProps.data) }}
                    </template>
                </Column>
                <Column header="Last Seen" field="last_seen">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.last_seen">{{ slotProps.data.last_seen }}</span>
                        <span v-else>Never</span>
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <ScannerUpdateDialog :scanner="slotProps.data" @object-updated="getItems"></ScannerUpdateDialog>
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
