<script>
import TargetCreateDialog from '@/components/dialogs/attack_surface/TargetCreateDialog.vue';
import TargetUpdateDialog from '@/components/dialogs/attack_surface/TargetUpdateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import {DataTypeChoices, InScopeChoices} from "@/utils/constants";

export default {
    name: 'TargetList',
    components: {
        GenericDataTable,
        BaseListLayout,
        TargetUpdateDialog,
        TargetCreateDialog
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Targets',
                    disabled: true
                }
            ],
            items: [],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            selectedItems: [],

            tagChoices: [],
            techChoices: [],
            deleteButtonLoading: false,
            dataTypeChoices: [
                { name: 'Domain', value: 'Domain' },
                { name: 'Subdomain', value: 'Subdomain' },
                { name: 'IP', value: 'IP' }
            ],
            filters: {
                data_type: { value: null },
                scope: { value: null }
            }
        };
    },
    methods: {
        InScopeChoices() {
            return InScopeChoices
        },
        DataTypeChoices() {
            return DataTypeChoices
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
                        this.$api.delete(this.$api.e.asTargetDetail, {pk: item.pk}).then(() => {
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
        onSort(event) {
            this.loading = true;
            let params = {
                ordering: event.sortField
            };
            if (event.sortOrder === -1) {
                params['ordering'] = `-${event.sortField}`;
            }
            this.$api
                .get(this.$api.e.asTargetList, null, params)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getItems() {
            this.loading = true;
            let data = {
                limit: this.pagination.limit,
                page: this.pagination.page,
                data_type: this.filters.data_type.value,
                scope: this.filters.scope.value
            };
            this.$api
                .get(this.$api.e.asTargetList, null, data)
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
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.$api
                .get(this.$api.e.asTargetList, null, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this target?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.asTargetDetail, {pk: id}).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Target was removed!',
                            life: 3000
                        });
                        this.getItems();
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
        <template #create-button>
            <TargetCreateDialog @object-created="getItems"></TargetCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No targets found!"
                blank-slate-title="No Targets!"
                blank-slate-icon="fa fa-crosshairs"
                :model-value="items"
                @sort="onSort"
                @filter="getItems"
                v-model:filters="filters"
                @page="onPage"
                :removable-sort="true"
                filter-display="menu"
                :show-search="true"
                @search="onGlobalSearch"
                :show-refresh-button="true"
                @refresh="getItems"
                v-model:selection="selectedItems"
            >
                <template #bulk-edit>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
                </template>
                <Column selectionMode="multiple" headerStyle=""></Column>

                <Column field="data" header="Data"></Column>
                <Column field="data_type" header="Data Type" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Select v-model="filterModel.value" :options="DataTypeChoices()" :showClear="true" optionLabel="name" optionValue="value"></Select>
                    </template>
                </Column>
                <Column header="IP">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.resolved_ip">{{ slotProps.data.resolved_ip }}</span>
                        <span v-else>-</span>
                    </template>
                </Column>
                <Column field="date_updated" header="Updated" sortable></Column>
                <Column field="scope" header="Scope" :show-filter-match-modes="false">
                    <template #filter="{ filterModel }">
                        <Select v-model="filterModel.value" :options="InScopeChoices()" optionValue="value" optionLabel="name"></Select>
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <TargetUpdateDialog :target="slotProps.data" @object-updated="getItems"></TargetUpdateDialog>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
