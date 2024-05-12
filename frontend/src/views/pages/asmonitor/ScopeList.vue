<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';
import ScopeCreateDialog from '@/components/asmonitor/dialogs/ScopeCreateDialog.vue';

export default {
    name: 'ScopeList',
    components: { ScopeCreateDialog, GenericDataTable, BaseListLayout },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Scope',
                    disabled: true
                }
            ],
            service: new ASMonitorService(),
            items: [],
            pagination: { page: 1, limit: 25 },
            loading: false,
            totalRecords: 0,
            programId: this.$route.params.programId
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.loading = true;
            let data = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service
                .getScopes(this.$api, this.programId, data)
                .then((resp) => {
                    this.totalRecords = resp.data.count;
                    this.items = resp.data.results;
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
            this.loading = true;
            let params = {
                search: query
            };
            this.service
                .getScopes(this.$api, this.programId, params)
                .then((resp) => {
                    this.totalRecords = resp.data.count;
                    this.items = resp.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this scope?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteScope(this.$api, this.programId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Scope was removed!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ScopeCreateDialog @object-created="getItems"></ScopeCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No scopes found!"
                blank-slate-title="No Scopes!"
                blank-slate-icon="fa fa-network-wired"
                :model-value="items"
                @search="onSearch"
                :show-search="true"
            >
                <Column field="data" header="Data"></Column>
                <Column field="scope_type" header="Scope Type"></Column>
                <Column field="date_updated" header="Updated"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
