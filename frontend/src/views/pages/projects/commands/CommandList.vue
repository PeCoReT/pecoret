<script>
import ProjectCommandService from '@/service/ProjectCommandService';
import ProjectCommandCreate from '@/components/dialogs/ProjectCommandCreate.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import CommandUpdate from '@/components/dialogs/CommandUpdate.vue';

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
        onSort() {},
        onFilter() {},
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
                .getItems(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { CommandUpdate, BlankSlate, ProjectCommandCreate }
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
            <div class="justify-content-start flex"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <ProjectCommandCreate @object-created="getItems"></ProjectCommandCreate>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable
                    :paginator="true"
                    dataKey="pk"
                    :rows="pagination.limit"
                    :value="items"
                    :rowHover="items.length > 0"
                    filterDisplay="menu"
                    :lazy="true"
                    responsiveLayout="scroll"
                    :totalRecords="totalRecords"
                    :loading="loading"
                    @page="onPage"
                    @sort="onSort"
                    @filter="onFilter"
                >
                    <template #header>
                        <div class="grid">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </template>
                    <template #empty>
                        <BlankSlate title="No commands!" text="No commands here!" icon="fa fa-terminal"></BlankSlate>
                    </template>
                    <Column field="command" header="Command"></Column>
                    <Column field="user.username" header="User"></Column>
                    <Column field="date_run" header="Date Run"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <CommandUpdate :command="slotProps.data" @object-updated="getItems"></CommandUpdate>
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"> </Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>