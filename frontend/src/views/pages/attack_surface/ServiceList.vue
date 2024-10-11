<script>
import ASMonitorService from '@/service/ASMonitorService';
import { useListViewComposable } from '@/composables/listViewComposable';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ASServiceCreateDialog from '@/components/dialogs/attack_surface/ServiceCreateDialog.vue';
import ScanFindingBulkEditDialog from '@/components/dialogs/attack_surface/ScanFindingBulkEditDialog.vue';

export default {
    name: 'ServiceList',
    components: { ScanFindingBulkEditDialog, ASServiceCreateDialog, GenericDataTable, BaseListLayout },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Services',
                    disabled: true
                }
            ],
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            filters: {},
            service: new ASMonitorService(),
            deleteButtonLoading: false,
            selectedItems: [],
            listComposable: useListViewComposable()
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        bulkDeleteConfirm() {
            this.$confirm.require({
                message: 'Do you want to delete all selected items?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteButtonLoading = true;
                    this.loading = true;
                    let itemsDeleted = 0;
                    this.selectedItems.forEach((item) => {
                        this.service.deleteService(item.pk).then(() => {
                            itemsDeleted++;
                            if (itemsDeleted === this.selectedItems.length) {
                                this.loading = false;
                                this.deleteButtonLoading = false;
                                this.selectedItems = [];
                                this.getItems();
                            }
                        });
                    });
                }
            });
        },
        getItems(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.service
                .getServices(data)
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
        }
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ASServiceCreateDialog @object-created="getItems"></ASServiceCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                v-model:selection="selectedItems"
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No services found!"
                blank-slate-title="No Services!"
                blank-slate-icon="fa fa-network"
                :model-value="this.items"
                @page="onPage"
                :show-search="true"
            >
                <template #bulk-edit>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
                </template>
                <Column selectionMode="multiple" headerStyle=""></Column>

                <Column field="target.data" header="Target"></Column>
                <Column header="Port" field="port_number"></Column>
                <Column header="Scheme" field="scheme"></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
