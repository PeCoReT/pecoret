<script>
import MobileApplicationCreateDialog from '@/components/projects/assets/MobileApplicationCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'MobileApplicationList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            breadcrumbs: [
                {
                    label: 'Mobile Applications',
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
            this.$api
                .get(this.$api.e.pMobileAppList, { projectPk: this.projectId }, params)
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
            this.$api
                .get(this.$api.e.pMobileAppList, { projectPk: this.projectId }, params)
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
                name: 'MobileApplicationDetail',
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
                message: 'Do you want to delete this application?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.pMobileAppDetail, { projectPk: this.projectId, pk: id }).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Mobile application was deleted!',
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
    components: { GenericDataTable, BaseListLayout, MobileApplicationCreateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <MobileApplicationCreateDialog @object-created="getItems"></MobileApplicationCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No mobile applications found!"
                blank-slate-title="No Mobile Applications!"
                blank-slate-icon="fa fa-mobile-screen"
                :model-value="items"
                @row-click="onRowClick"
                @page="onPage"
            >
                <template #header>
                    <div class="flex justify-content-between flex-column sm:flex-row">
                        <IconField iconPosition="left">
                            <InputIcon class="fa fa-search"></InputIcon>
                            <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                        </IconField>
                    </div>
                </template>
                <Column field="name" header="Name"></Column>
                <Column field="os" header="Operating System"></Column>
                <Column field="version" header="Version"></Column>
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
