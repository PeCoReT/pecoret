<script>
import BlankSlate from '@/components/BlankSlate.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import { useListViewComposable } from '@/composables/listViewComposable';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import AssetBulkEditDialog from '@/components/dialogs/AssetBulkEditDialog.vue';

export default {
    name: 'AssetList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            breadcrumbs: [
                {
                    label: 'Assets',
                    disabled: true
                }
            ],
            items: [],
            loading: false,
            filters: {},
            totalRecords: 0,
            selectedItems: [],
            deleteButtonLoading: false,
            pagination: { page: 1, limit: 20 },
            listComposable: useListViewComposable()
        };
    },
    methods: {
        onGlobalSearch(query) {
            this.getItems({ search: query });
        },
        getItems(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pAssetList, { pPk: this.projectId }, data)
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
        bulkDelete() {
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
                            .delete(this.$api.e.pAssetDetail, {
                                pPk: this.projectId,
                                pk: item.pk
                            })
                            .then(() => {
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
        getAssetLink(pk) {
            return this.$router.resolve({
                name: 'AssetDetail',
                params: {
                    projectId: this.projectId,
                    assetId: pk
                }
            }).href;
        }
    },
    mounted() {
        this.getItems();
    },
    components: { AssetBulkEditDialog, GenericDataTable, BaseListLayout, BlankSlate }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <Button icon="fa fa-plus" label="Asset" outlined @click="this.$router.push({ name: 'AssetCreate', params: { projectId: this.projectId } })"></Button>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-icon="fa fa-earth-europe"
                blank-slate-text="No assets found!"
                blank-slate-title="No Assets!"
                :show-search="true"
                @search="onGlobalSearch"
                @page="onPage"
                v-model:selection="selectedItems"
                v-model="items"
            >
                <template #bulk-edit>
                    <AssetBulkEditDialog :items="selectedItems" @object-updated="getItems"></AssetBulkEditDialog>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDelete" class="ml-2 mb-2"></Button>
                </template>
                <Column selectionMode="multiple" headerStyle=""></Column>

                <Column field="name" header="Name">
                    <template #body="slotProps">
                        <a :href="this.getAssetLink(slotProps.data.pk)" class="underline">{{ slotProps.data.name }}</a>
                    </template>
                </Column>
                <Column field="name" header="Name"></Column>
                <Column field="asset_type.name" header="Asset Type"></Column>
                <Column field="environment" header="Environment"></Column>
                <Column field="accessible" header="Accessible"></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
