<script>
import ProjectCommandService from '@/service/ProjectCommandService';
import ProjectCommandCreate from '@/components/dialogs/ProjectCommandCreate.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import CommandUpdate from '@/components/dialogs/CommandUpdate.vue';
import BaseListLayout from "@/layout/base/BaseListLayout.vue";
import GenericDataTable from "@/components/common/GenericDataTable.vue";

export default {
    name: 'CommandList',
    mounted() {
        this.getItems();
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Commands',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            service: new ProjectCommandService(),
            items: [],
            selectedItems: [],
            deleteButtonLoading: false,
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 }
        };
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service
                .getCommands(this.$api, this.projectId, params)
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
                message: 'Do you want to delete this command?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteCommand(this.$api, this.projectId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Command was deleted!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
        onGlobalSearch(search) {
            this.loading = true;
            let params = {
                search: search
            };
            this.service
                .getCommands(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {GenericDataTable, BaseListLayout, CommandUpdate, BlankSlate, ProjectCommandCreate }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
                            <ProjectCommandCreate @object-created="getItems"></ProjectCommandCreate>

        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No commands found!"
                blank-slate-title="No Commands!"
                blank-slate-icon="fa fa-terminal"
                :model-value="items"
                :show-search="true"
                @search="onGlobalSearch"
            >
                 <Column field="command" header="Command"></Column>
                    <Column field="user.username" header="User"></Column>
                    <Column field="date_run" header="Date Run"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <CommandUpdate :command="slotProps.data" @object-updated="getItems"></CommandUpdate>
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"> </Button>
                        </template>
                    </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>