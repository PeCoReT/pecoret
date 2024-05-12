<script>
import ASMonitorService from '@/service/ASMonitorService';
import FindingCreateDialog from '@/components/asmonitor/FindingCreateDialog.vue';
import SeverityBadge from '@/components/SeverityBadge.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';
import FindingBulkEditDialog from '@/components/asmonitor/dialogs/FindingBulkEditDialog.vue';
import TagBadgeButton from '@/components/asmonitor/TagBadgeButton.vue';

export default {
    name: 'FindingList',
    components: { TagBadgeButton, FindingBulkEditDialog, GenericDataTable, BaseListLayout, FindingCreateDialog, SeverityBadge },
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

            programId: this.$route.params.programId,
            targetChoices: [],
            filters: {
                'host.ip': { value: null },
                status: { value: null },
                severity: { value: null }
            }
        };
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                host: this.filters['host.ip'].value,
                status: this.filters.status.value,
                page: this.pagination.page,
                limit: this.pagination.limit,
                severity: this.filters.severity.value
            };
            this.service
                .getFindings(this.$api, this.programId, params)
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
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.service
                .getFindings(this.$api, this.programId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onRowClick(row) {
            this.$router.push({
                name: 'ASMonitorFindingDetail',
                params: { programId: this.programId, findingId: row.data.pk }
            });
        },
        targetFilter(event) {
            let params = {
                search: event.value
            };
            this.service.getTargets(this.$api, this.programId, params).then((response) => {
                this.targetChoices = response.data.results;
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this finding?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteFinding(this.$api, this.programId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Finding was removed!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
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
                        this.service.deleteFinding(this.$api, this.programId, item.pk).then(() => {
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
        <template #create-button>
            <FindingCreateDialog @object-created="getItems"></FindingCreateDialog>
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
                @row-click="onRowClick"
                @filter="getItems"
                filterDisplay="menu"
                :show-search="true"
                v-model:selection="selectedItems"
                @search="onGlobalSearch"
            >
                <template #bulk-edit>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2 mb-2"></Button>
                    <FindingBulkEditDialog :findings="selectedItems" @object-updated="getItems" :programId="this.programId"></FindingBulkEditDialog>
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
                <Column field="host.ip" header="Host" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="targetChoices" @filter="targetFilter" placeholder="Select host" filter @focus="targetFilter" class="p-column-filter" showClear optionLabel="ip" optionValue="pk"></Dropdown>
                    </template>
                </Column>
                <Column field="status" header="Status" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="service.getStatusChoices()" class="p-column-filter" showClear optionLabel="name" optionValue="value"></Dropdown>
                    </template>
                </Column>
                <Column field="tags" header="Tags" :showFilterMatchModes="false">
                    <template #body="slotProps">
                        <TagBadgeButton :label="tag" v-for="tag in slotProps.data.tags" :key="tag.pk"></TagBadgeButton>
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
