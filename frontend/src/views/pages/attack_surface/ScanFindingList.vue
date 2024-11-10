<script>
import ScanFindingCreateDialog from '@/components/dialogs/attack_surface/ScanFindingCreateDialog.vue';
import SeverityBadge from '@/components/badges/SeverityBadge.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ScanFindingBulkEditDialog from '@/components/dialogs/attack_surface/ScanFindingBulkEditDialog.vue';
import TagBadgeButton from '@/components/badges/TagBadgeButton.vue';
import { useListViewComposable } from '@/composables/listViewComposable';
import {asFindingStatusChoices, severityChoices} from "@/utils/constants";

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
            items: [],
            selectedItems: [],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            deleteButtonLoading: false,
            listComposable: useListViewComposable(),
            filters: {
                status: { value: 'Open' },
                severity: { value: null }
            }
        };
    },
    methods: {
        asFindingStatusChoices() {
            return asFindingStatusChoices
        },
        severityChoices() {
            return severityChoices
        },
        getItems(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asScanFindingList, null, data)
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
            this.getItems({ search: query });
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
                        this.$api.delete(this.$api.e.asScanFindingDetail, { pk: item.pk }).then(() => {
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
        <template #head-left> There are {{ totalRecords }} findings</template>
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
                @sort="
                    (event) => {
                        listComposable.sort(event, this.getItems);
                    }
                "
                :removable-sort="true"
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
                        <Dropdown v-model="filterModel.value" :options="severityChoices()" class="p-column-filter" showClear optionLabel="name" optionValue="value"></Dropdown>
                    </template>
                </Column>
                <Column field="affected_component" header="Component"></Column>
                <Column field="program.name" header="Program"></Column>
                <Column field="status" header="Status" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="asFindingStatusChoices()" class="p-column-filter" showClear optionLabel="name" optionValue="value"></Dropdown>
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
                <Column field="date_created" header="Created" sortable></Column>
                <Column field="date_updated" header="Updated" sortable></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
