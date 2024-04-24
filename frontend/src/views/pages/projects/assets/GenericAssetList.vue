<script>
import AssetService from '@/service/AssetService';
import GenericAssetCreateDialog from '@/components/projects/assets/GenericAssetCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'HostList',
    data() {
        return {
            service: new AssetService(),
            projectId: this.$route.params.projectId,
            breadcrumbs: [
                {
                    label: 'Generic Assets',
                    disabled: true
                }
            ],
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 }
        };
    },
    methods: {
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.service
                .getGenericAssets(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getItems() {
            this.loading = true;
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.service
                .getGenericAssets(this.$api, this.projectId, params)
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
                    this.assetService.deleteGenericAsset(this.$api, this.projectId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Host was deleted!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
        onRowClick(row) {
            this.$router.push({
                name: 'GenericAssetDetail',
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
    components: { GenericDataTable, BaseListLayout, GenericAssetCreateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <GenericAssetCreateDialog @object-created="getItems"></GenericAssetCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No assets found!"
                blank-slate-title="No Assets!"
                blank-slate-icon="fa fa-server"
                :model-value="items"
                @page="onPage"
                @rowClick="onRowClick"
            >
                <template #header>
                    <div class="grid">
                        <IconField iconPosition="left">
                            <InputIcon class="fa fa-search"></InputIcon>
                            <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                        </IconField>
                    </div>
                </template>

                <Column field="name" header="Name"></Column>
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
