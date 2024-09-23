<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import { useListViewComposable } from '@/composables/listViewComposable';
import ScanTypeUpdateDialog from '@/components/dialogs/attack_surface/admin/ScanTypeUpdateDialog.vue';
import ScanTypeCreateDialog from '@/components/dialogs/attack_surface/admin/ScanTypeCreateDialog.vue';

export default {
    name: 'ASScanTypeList.vue',
    components: { ScanTypeCreateDialog, ScanTypeUpdateDialog, GenericDataTable, BaseListLayout },
    data() {
        return {
            service: new ASMonitorService(),
            breadcrumbs: [
                {
                    label: 'Scan Types',
                    disabled: true
                }
            ],
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            filters: {},
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
                .getScanTypes(data)
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
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this scan type?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteScanType(id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Scan Type was removed!',
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
            <ScanTypeCreateDialog @object-created="getItems"></ScanTypeCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No scan types found!"
                blank-slate-title="No Scan Types!"
                blank-slate-icon="fa fa-layer-group"
                :model-value="items"
                @page="onPage"
                @search="onSearch"
                :show-search="true"
            >
                <Column header="Name" field="name"></Column>
                <Column field="allowed_object_type" header="Allowed Object Type"></Column>
                <Column field="can_run_manually" header="Can Run Manually?"></Column>
                <Column field="conditions" header="Conditions"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <ScanTypeUpdateDialog :scan-type="slotProps.data" @object-updated="getItems"></ScanTypeUpdateDialog>
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
