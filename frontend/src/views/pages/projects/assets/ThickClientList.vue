<script>
import AssetService from '@/service/AssetService';
import BlankSlate from '@/components/BlankSlate.vue';
import ThickClientCreateDialog from '@/components/dialogs/ThickClientCreateDialog.vue';

export default {
    name: 'ThickClientList',
    data() {
        return {
            assetService: new AssetService(),
            projectId: this.$route.params.projectId,
            breadcrumbs: [
                {
                    label: 'ThickClients',
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
                .getThickClients(this.$api, this.projectId, params)
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
                .getThickClients(this.$api, this.projectId, params)
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
                message: 'Do you want to delete this thick client?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.assetService.deleteThickClient(this.$api, this.projectId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Thick client was deleted!',
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
    components: { ThickClientCreateDialog, BlankSlate }
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
                <ThickClientCreateDialog @object-created="getItems"></ThickClientCreateDialog>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable
                    paginator
                    dataKey="pk"
                    lazy
                    :rows="pagination.limit"
                    :value="items"
                    filterDisplay="menu"
                    responsiveLayout="scroll"
                    @sort="onSort"
                    @filter="onFilter"
                    @page="onPage"
                    :totalRecords="totalRecords"
                    :loading="loading"
                    :rowHover="items.length > 0"
                >
                    <template #header>
                        <div class="flex justify-content-between flex-column sm:flex-row">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </template>
                    <template #empty>
                        <BlankSlate icon="fa fa-laptop" title="No thick clients!" text="No thick clients found!"></BlankSlate>
                    </template>

                    <Column field="name" header="Name">
                        <template #body="slotProps">
                            <router-link class="text-color underline" :to="{ name: 'ThickClientDetail', params: { projectId: this.projectId, assetId: slotProps.data.pk } }">
                                {{ slotProps.data.name }}
                            </router-link>
                        </template>
                    </Column>
                    <Column field="os" header="Operating System"></Column>
                    <Column field="version" header="Version"></Column>
                    <Column field="programming_language" header="Programming Language"></Column>
                    <Column field="decompile_allowed" header="Decompile?"></Column>
                    <Column field="environment" header="Environment"></Column>
                    <Column field="accessible" header="Accessible"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>
