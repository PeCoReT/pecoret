<script>
import ASMonitorService from '@/service/ASMonitorService';
import { useListViewComposable } from '@/composables/listViewComposable';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ASServiceCreateDialog from '@/components/dialogs/attack_surface/ServiceCreateDialog.vue';

export default {
    name: 'ServiceList',
    components: { ASServiceCreateDialog, GenericDataTable, BaseListLayout },
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
            <GenericDataTable :total-records="totalRecords" :loading="loading" :pagination="pagination" blank-slate-text="No services found!" blank-slate-title="No Services!" blank-slate-icon="fa fa-network" :model-value="this.items" @page="onPage">
                <Column field="target.data" header="Target"></Column>
                <Column header="Port" field="port.display"></Column>
                <Column header="Scheme" field="scheme"></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
