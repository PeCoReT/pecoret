<script>
import ProjectScopeCreateDialog from '@/components/dialogs/ProjectScopeCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'ScopeList',
    mounted() {
        this.getItems();
    },
    data() {
        return {
            breadcrumbs: [{ label: 'Scopes', disabled: true }],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
        };
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to delete this scope?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteScope(id);
                }
            });
        },
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.$api
                .get(this.$api.e.pScopeList, { projectPk: this.projectId }, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        deleteScope(id) {
            this.$api.delete(this.$api.e.pScopeDetail, { projectPk: this.projectId, pk: id }).then(() => {
                this.$toast.add({
                    severity: 'info',
                    summary: 'Deleted',
                    detail: 'Scope was deleted!',
                    life: 3000
                });
                this.getItems();
            });
        },
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.$api
                .get(this.$api.e.pScopeList, { projectPk: this.projectId }, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { GenericDataTable, BaseListLayout, ProjectScopeCreateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ProjectScopeCreateDialog @object-created="getItems"></ProjectScopeCreateDialog>
        </template>
        <template #table>
            <GenericDataTable :total-records="totalRecords" :loading="loading" :pagination="pagination" blank-slate-text="No scopes found!" blank-slate-title="No Scopes!" blank-slate-icon="fa fa-star" :model-value="items" @page="onPage">
                <Column field="details" header="Details"></Column>
                <Column field="permission" header="Permission"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
