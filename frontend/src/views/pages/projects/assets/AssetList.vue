<script>
import BlankSlate from '@/components/BlankSlate.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import {useListViewComposable} from "@/composables/listViewComposable";
import AssetCreateDialog from "@/components/projects/assets/AssetCreateDialog.vue";

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
            pagination: { page: 1, limit: 20 },
            listComposable: useListViewComposable()
        };
    },
    methods: {
        onGlobalSearch(query) {
            this.getItems({search: query})
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
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: 'Do you want to delete this asset?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.pAssetDetail, { pPk: this.projectId, pk: id }).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Asset was deleted!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
        onRowClick(row) {
            this.$router.push({
                name: 'AssetDetail',
                params: {
                    projectId: this.projectId,
                    assetId: row.data.pk
                }
            });
        }
    },
    mounted() {
        this.getItems();
    },
    components: {AssetCreateDialog, BaseListLayout, BlankSlate }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <AssetCreateDialog @object-created="getItems"></AssetCreateDialog>
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
                @row-click="onRowClick"
                @page="onPage"
                v-model="items"
            >
                <Column field="name" header="Name">
                    <template #body="slotProps">
                        {{ slotProps.data.name }}
                    </template>
                </Column>
                <Column field="name" header="Name"></Column>
                <Column field="asset_type.name" header="Asset Type"></Column>
                <Column field="environment" header="Environment"></Column>
                <Column field="accessible" header="Accessible"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
