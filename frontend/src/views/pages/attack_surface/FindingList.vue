<script>
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import ASFindingCreateDialog from '@/components/dialogs/attack_surface/FindingCreateDialog.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import { useListViewComposable } from '@/composables/listViewComposable';

export default {
    name: 'FindingList',
    components: { GenericDataTable, ASFindingCreateDialog, BaseListLayout },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Findings'
                }
            ],
            items: [],
            totalRecords: 0,
            loading: false,
            pagination: { page: 1, limit: 20 },
            filters: {},
            selectedItems: [],
            downloadButtonLoading: false,

            listComposable: useListViewComposable()
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
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
                        this.$api.delete(this.$api.e.asFindingDetail, { pk: item.pk }).then(() => {
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
        getItems(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asFindingList, null, data)
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
        onSearch(query) {
            this.getItems({ search: query });
        },
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ASFindingCreateDialog @object-created="getItems"></ASFindingCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No Findings here!"
                blank-slate-title="No Findings!"
                blank-slate-icon="fa fa-bugs"
                :model-value="items"
                @page="onPage"
                :show-search="true"
                @search="onSearch"
                v-model:selection="selectedItems"
            >
                <template #bulk-edit>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2" :loading="downloadButtonLoading"></Button>
                </template>
                <Column selectionMode="multiple" headerStyle=""></Column>

                <Column header="Title" field="title">
                    <template #body="slotProps">
                        <a :href="this.$router.resolve({name: 'AttackSurfaceFindingUpdate', params: {findingId: slotProps.data.pk}}).href" class="underline">{{ slotProps.data.title }}</a>
                    </template>
                </Column>
                <Column header="Created By?" field="created_by_user.username"></Column>
                <Column header="Status" field="status"></Column>
                <Column header="Severity" field="severity">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.severity">{{ slotProps.data.severity }}</span>
                        <span v-else>-</span>
                    </template>
                </Column>
                <Column header="Date Updated?" field="date_updated"> </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
