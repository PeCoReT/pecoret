<script>
import ASMonitorService from '@/service/ASMonitorService';
import FindingCreateDialog from '@/components/asmonitor/FindingCreateDialog.vue';
import SeverityBadge from '@/components/SeverityBadge.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'FindingList',
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
            programId: this.$route.params.programId,
            targetChoices: [],
            filters: {
                target: { value: null },
                'target.name': { value: null }
            }
        };
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                target: this.filters['target.name'].value
            };
            this.service
                .getFindings(this.$api, this.programId, params)
                .then((response) => {
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
                @search="onGlobalSearch"
            >
                <Column field="name" header="Name"></Column>
                <Column field="severity" header="Severity">
                    <template #body="slotProps">
                        <SeverityBadge :severity="slotProps.data.severity"></SeverityBadge>
                    </template>
                </Column>
                <Column field="target.name" header="Target" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="targetChoices" @filter="targetFilter" placeholder="Select target" filter @focus="targetFilter" class="p-column-filter" showClear optionLabel="name" optionValue="pk"></Dropdown>
                    </template>
                </Column>
                <Column field="status" header="Status"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
