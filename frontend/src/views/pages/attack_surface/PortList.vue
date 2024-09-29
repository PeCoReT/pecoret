<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';


export default {
    name: 'PortList',
    components: {
        GenericDataTable,
        BaseListLayout
    },
    data() {
        return {
            service: new ASMonitorService(),
            items: [],
            loading: false,
            pagination: { limit: 25, page: 1 },
            totalRecords: 0,
            deleteButtonLoading: false,
            selectedItems: [],
            filters: {
                port: { value: null },
                'target.program.name': { value: null },
                service: { value: null }
            },
            breadcrumbs: [
                {
                    label: 'Ports',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit,
                number: this.filters.port.value,
                service_name: this.filters.service.value
            };
            this.service
                .getPorts(params)
                .then((resp) => {
                    this.items = resp.data.results;
                    this.totalRecords = resp.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onSearch(event) {
            let params = {
                search: event
            };
            this.service.getPorts(params).then((resp) => {
                this.items = resp.data.results;
                this.totalRecords = resp.data.count;
            });
        },
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
                        this.service.deletePort(item.pk).then(() => {
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
        }
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No ports found!"
                blank-slate-title="No Ports"
                blank-slate-icon="fa fa-circle-nodes"
                :model-value="items"
                :show-search="true"
                @search="onSearch"
                :show-refresh-button="true"
                @refresh="getItems"
                v-model:filters="filters"
                @filter="getItems"
                filter-display="menu"
                v-model:selection="selectedItems"
            >
                <template #bulk-edit>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
                </template>
                <Column selection-mode="multiple" headerStyle=""></Column>
                <Column field="number" header="Port" :show-filter-match-modes="false">
                    <template #filter="{ filterModel }">
                        <InputText v-model="filterModel.value"></InputText>
                    </template>
                </Column>
                <Column field="protocol" header="Protocol"></Column>
                <Column header="Service" :show-filter-match-modes="false">
                    <template #filter="{ filterModel }">
                        <InputText v-model="filterModel.value"></InputText>
                    </template>
                    <template #body="slotProps">
                        <span v-if="slotProps.data.service_name">{{ slotProps.data.service_name }}</span>
                        <span v-else>-</span>
                    </template>
                </Column>
                <Column field="host.ip_address" header="Host"></Column>
                <Column field="date_created" header="Created"></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
