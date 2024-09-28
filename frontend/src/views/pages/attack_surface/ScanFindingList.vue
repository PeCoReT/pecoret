<script>
import ASMonitorService from '@/service/ASMonitorService';
import ScanFindingCreateDialog from '@/components/dialogs/attack_surface/ScanFindingCreateDialog.vue';
import SeverityBadge from '@/components/badges/SeverityBadge.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ScanFindingBulkEditDialog from '@/components/dialogs/attack_surface/ScanFindingBulkEditDialog.vue';
import TagBadgeButton from '@/components/badges/TagBadgeButton.vue';

export default {
    name: 'ScanFindingList',
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
                    label: 'Findings',
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
            filters: {
                status: { value: 'Open' },
                severity: { value: null }
            }
        };
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                status: this.filters.status.value,
                page: this.pagination.page,
                limit: this.pagination.limit,
                severity: this.filters.severity.value
            };
            this.service
                .getScanFindings(this.$api, params)
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
                name: 'AttackSurfaceScanFindingDetail',
                params: { findingId: row.data.pk }
            });
        },
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query,
                status: this.filters.status.value,
                severity: this.filters.severity.value
            };
            this.service
                .getScanFindings(this.$api, params)
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
                        this.service.deleteScanFinding(this.$api, item.pk).then(() => {
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
        <template #head-left> There are {{ totalRecords }} findings </template>
        <template #create-button>
            <ScanFindingCreateDialog @object-created="getItems"></ScanFindingCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No findings here!"
                blank-slate-title="No Findings!"
                blank-slate-icon="fa fa-bugs"
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
                    <ScanFindingBulkEditDialog :findings="selectedItems" @object-updated="getItems"></ScanFindingBulkEditDialog>
                </template>
                <Column selectionMode="multiple" headerStyle=""></Column>
                <Column field="name" header="Name"></Column>
                <Column field="severity" header="Severity" :show-filter-match-modes="false">
                    <template #body="slotProps">
                        <SeverityBadge :severity="slotProps.data.severity"></SeverityBadge>
                    </template>
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="service.getSeverityChoices()" class="p-column-filter" showClear optionLabel="name" optionValue="value"></Dropdown>
                    </template>
                </Column>
                <Column field="affected_component" header="Component"></Column>
                <Column field="program.name" header="Program"></Column>
                <Column field="status" header="Status" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="service.getStatusChoices()" class="p-column-filter" showClear optionLabel="name" optionValue="value"></Dropdown>
                    </template>
                </Column>
                <Column field="tags" header="Tags" :showFilterMatchModes="false">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.tags && slotProps.data.tags.length > 0">
                            <TagBadgeButton :label="tag" v-for="tag in slotProps.data.tags" :key="tag.pk"></TagBadgeButton>
                        </span>
                        <span v-else>-</span>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
