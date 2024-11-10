<script>
import WebApplicationCreateDialog from '@/components/projects/assets/WebApplicationCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';

export default {
    name: 'WebApplicationList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            breadcrumbs: [
                {
                    label: 'Web Applications',
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
                .get(this.$api.e.pWebAppList, { projectPk: this.projectId }, params)
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
                .get(this.$api.e.pWebAppList, { projectPk: this.projectId }, params)
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
                message: 'Do you want to delete this web application?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.pWebAppList, { projectPk: this.projectId, pk: id }).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Web application was deleted!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
        onRowClick(row) {
            this.$router.push({
                name: 'WebApplicationDetail',
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
    components: { BaseListLayout, WebApplicationCreateDialog, BlankSlate }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <WebApplicationCreateDialog @object-created="getItems"></WebApplicationCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-icon="fa fa-earth-europe"
                blank-slate-text="No web applications found!"
                blank-slate-title="No Web Applications!"
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
                <Column field="base_url" header="Base URL"></Column>
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
