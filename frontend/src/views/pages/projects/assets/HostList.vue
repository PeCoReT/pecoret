<script>
import AssetService from '@/service/AssetService';
import HostCreateDialog from '@/components/projects/assets/HostCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'HostList',
    data() {
        return {
            assetService: new AssetService(),
            projectId: this.$route.params.projectId,
            breadcrumbs: [
                {
                    label: 'Hosts',
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
            this.assetService
                .getHosts(this.$api, this.projectId, params)
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
            this.assetService
                .getHosts(this.$api, this.projectId, params)
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
                name: 'HostDetail',
                params: {
                    projectId: this.projectId,
                    assetId: row.data.pk
                }
            });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: 'Do you want to delete this host?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.assetService.deleteHost(this.$api, this.projectId, id).then(() => {
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
        }
    },
    mounted() {
        this.getItems();
    },
    components: { GenericDataTable, BaseListLayout, HostCreateDialog,  }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <HostCreateDialog @object-created="getItems"></HostCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No hosts found!"
                blank-slate-title="No Hosts!"
                blank-slate-icon="fa fa-server"
                :model-value="this.items"
                @rowClick="onRowClick"
                @page="onPage"
            >
                <template #header>
                    <div class="grid">
                        <IconField iconPosition="left">
                            <InputIcon class="fa fa-search"></InputIcon>
                            <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                        </IconField>
                    </div>
                </template>

                <Column field="ip" header="IP"></Column>
                <Column field="dns" header="DNS"></Column>
                <Column field="operating_system" header="Operating System"></Column>
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
