<script>
import ASMonitorService from '@/service/ASMonitorService';
import FindingCreateDialog from '@/components/asmonitor/FindingCreateDialog.vue';
import SeverityBadge from '@/components/SeverityBadge.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'GlobalFindingList',
    components: { GenericDataTable, BaseListLayout, FindingCreateDialog, SeverityBadge },
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
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            filters: {
                status: { value: null },
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
                .getGlobalFindings(this.$api, params)
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
                .getGlobalFindings(this.$api, params)
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
                params: { programId: row.data.program.pk, findingId: row.data.pk }
            });
        },
        confirmDialogDelete(programId, id) {
            this.$confirm.require({
                message: 'Do you want to remove this finding?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteFinding(this.$api, programId, id).then(() => {
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
                @page="onPage"
                :show-search="true"
                @search="onGlobalSearch"
                @rowClick="onRowClick"
                filterDisplay="menu"
                v-model:filters="filters"
                @filter="getItems"
            >
                <Column field="name" header="Name"></Column>
                <Column field="severity" header="Severity" :show-filter-match-modes="false">
                    <template #body="slotProps">
                        <SeverityBadge :severity="slotProps.data.severity"></SeverityBadge>
                    </template>
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="service.getSeverityChoices()" class="p-column-filter" showClear optionLabel="name" optionValue="value"></Dropdown>
                    </template>
                </Column>
                <Column field="host.ip" header="Host"></Column>
                <Column field="status" header="Status" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="service.getStatusChoices()" class="p-column-filter" showClear optionLabel="name" optionValue="value"></Dropdown>
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.program.pk, slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
