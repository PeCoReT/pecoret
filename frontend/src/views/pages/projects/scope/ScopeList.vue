<script>
import ProjectScopeService from '@/service/ProjectScopeService';
import ProjectScopeCreateDialog from '@/components/dialogs/ProjectScopeCreateDialog.vue';
import BlankSlate from '../../../../components/BlankSlate.vue';

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
            service: new ProjectScopeService()
        };
    },
    methods: {
        onSort(event) {},
        onFilter(event) {},
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
            this.service
                .getScopes(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        deleteScope(id) {
            this.service.deleteScope(this.$api, this.projectId, id).then(() => {
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
            this.service
                .getScopes(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { BlankSlate, ProjectScopeCreateDialog }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <ProjectScopeCreateDialog @object-created="getItems"></ProjectScopeCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable paginator lazy dataKey="pk" :value="items" :rows="pagination.limit" :rowHover="items.length > 0" :totalRecords="totalRecords" filterDisplay="menu" :loading="loading" @sort="onSort" @page="onPage" @filter="onFilter">
                    <template #empty>
                        <BlankSlate icon="fa fa-star" text="No scopes!" title="No scopes found!"></BlankSlate>
                    </template>
                    <template #header>
                        <div class="flex justify-content-between flex-column sm:flex-row">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </template>
                    <Column field="details" header="Details"></Column>
                    <Column field="permission" header="Permission"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>