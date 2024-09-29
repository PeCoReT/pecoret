<script>
import ASMonitorService from '@/service/ASMonitorService';
import ScanFindingCreateDialog from '@/components/dialogs/attack_surface/ScanFindingCreateDialog.vue';
import SeverityBadge from '@/components/badges/SeverityBadge.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ScanFindingBulkEditDialog from '@/components/dialogs/attack_surface/ScanFindingBulkEditDialog.vue';
import TagBadgeButton from '@/components/badges/TagBadgeButton.vue';

export default {
    name: 'HostList',
    components: {
        TagBadgeButton,
        ScanFindingBulkEditDialog,
        GenericDataTable,
        BaseListLayout,
        ScanFindingCreateDialog,
        SeverityBadge
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Hosts',
                    disabled: true
                }
            ],
            service: new ASMonitorService(),
            items: [],
            selectedItems: [],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            deleteButtonLoading: false,
            filters: {}
        };
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.service
                .getHosts(params)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onRowClick(row) {
            this.$router.push({
                name: 'AttackSurfaceHostDetail',
                params: { hostId: row.data.pk }
            });
        },
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.service
                .getHosts(params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
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
                        this.service.deleteHost(item.pk).then(() => {
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
    },
    mounted() {
        this.getItems();
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
                blank-slate-text="No hosts here!"
                blank-slate-title="No Hosts!"
                blank-slate-icon="fa fa-server"
                :model-value="items"
                v-model:filters="filters"
                @page="onPage"
                @filter="getItems"
                filterDisplay="menu"
                :show-search="true"
                v-model:selection="selectedItems"
                @search="onGlobalSearch"
                :show-refresh-button="true"
                @refresh="getItems"
                @row-click="onRowClick"
            >
                <template #bulk-edit>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
                </template>
                <Column selectionMode="multiple" headerStyle=""></Column>
                <Column field="ip_address" header="IP"></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
