<script>
import SeverityBadge from '@/components/badges/SeverityBadge.vue';
import FindingCopyDialog from '@/components/dialogs/FindingCopyDialog.vue';
import AssetSelectField from '@/components/forms/fields/AssetSelectField.vue';
import FindingCreateDialog from '@/components/dialogs/FindingCreateDialog.vue';
import FindingBulkEditDialog from '@/components/projects/findings/FindingBulkEditDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import { useListViewComposable } from '@/composables/listViewComposable';

export default {
    name: 'FindingList',
    mounted() {
        this.getFindings();
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Findings',
                    disabled: true
                }
            ],
            filters: {
                needs_review: { value: null },
                asset: { value: null }
            },
            projectId: this.$route.params.projectId,
            findings: [],
            selectedItems: [],
            deleteButtonLoading: false,
            loading: false,
            totalRecords: 0,
            listComposable: useListViewComposable(),
            pagination: { page: 1, limit: 20 }
        };
    },
    methods: {
        getFindings(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pFindingList, { pPk: this.projectId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.findings = response.data.results;
                    this.selectedItems = [];
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onSort() {},
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getFindings();
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
                        this.$api
                            .delete(this.$api.e.pFindingDetail, {
                                pPk: this.projectId,
                                pk: item.pk
                            })
                            .then(() => {
                                itemsDeleted++;
                                if (itemsDeleted === this.selectedItems.length) {
                                    this.loading = false;
                                    this.deleteButtonLoading = false;
                                    this.selectedItems = [];
                                    this.getFindings();
                                }
                            });
                    });
                }
            });
        },
        onGlobalSearch(search) {
            this.loading = true;
            let params = {
                search: search
            };
            this.$api
                .get(this.$api.e.pFindingList, { pPk: this.projectId }, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.findings = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {
        GenericDataTable,
        BaseListLayout,
        FindingBulkEditDialog,
        FindingCreateDialog,
        AssetSelectField,
        FindingCopyDialog,
        SeverityBadge
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <FindingCreateDialog :project-id="this.projectId"></FindingCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No findings here!"
                blank-slate-title="No Findings!"
                blank-slate-icon="fa fa-bugs"
                :model-value="findings"
                v-model:filters="filters"
                v-model:selection="selectedItems"
                @page="onPage"
                @filter="getFindings"
                @sort="onSort"
                :filter="true"
                filter-display="menu"
                :show-refresh-button="true"
                @refresh="getFindings"
                :show-search="true"
                @search="onGlobalSearch"
            >
                <template #bulk-edit>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2 mb-2"></Button>
                    <FindingBulkEditDialog :findings="selectedItems" @object-updated="getFindings"></FindingBulkEditDialog>
                </template>
                <Column selectionMode="multiple" headerStyle=""></Column>

                <Column field="name" header="Name">
                    <template #body="slotProps">
                        <a :href="this.$router.resolve({ name: 'FindingDetail', params: { projectId: this.projectId, findingId: slotProps.data.pk } }).href" class="underline">{{ slotProps.data.name }}</a>
                    </template>
                </Column>
                <Column field="severity" header="Severity">
                    <template #body="slotProps">
                        <SeverityBadge :severity="slotProps.data.severity"></SeverityBadge>
                    </template>
                </Column>
                <Column field="asset.name" filterField="asset" header="Asset" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <AssetSelectField v-model="filterModel.value" :project-pk="this.projectId"></AssetSelectField>
                    </template>
                </Column>
                <Column field="vulnerability.name" header="Vulnerability"></Column>
                <Column field="unique_id" header="ID"></Column>
                <Column field="status" header="Status"></Column>
                <Column field="finding_date" header="Date"></Column>
                <Column field="needs_review" header="Needs Review" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Checkbox v-model="filterModel.value" indeterminate binary></Checkbox>
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <FindingCopyDialog :finding="slotProps.data.pk" @object-created="getFindings"></FindingCopyDialog>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
