<script>
import AssetService from '@/service/AssetService';
import WebApplicationCreateDialog from '@/components/projects/assets/WebApplicationCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'WebApplicationList',
    data() {
        return {
            assetService: new AssetService(),
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
            this.assetService
                .getWebApplications(this.$api, this.projectId, params)
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
                .getWebApplications(this.$api, this.projectId, params)
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
                    this.assetService.deleteWebApplication(this.$api, this.projectId, id).then(() => {
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
    components: { WebApplicationCreateDialog, BlankSlate }
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
                <WebApplicationCreateDialog @object-created="getItems"></WebApplicationCreateDialog>
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
                    :rowHover="items.length > 0"
                    responsiveLayout="scroll"
                    @page="onPage"
                    :totalRecords="totalRecords"
                    :loading="loading"
                    @row-click="onRowClick"
                >
                    <template #empty>
                        <BlankSlate icon="fa fa-earth-europe" title="No web applications!" text="No web applications found!"></BlankSlate>
                    </template>
                    <template #header>
                        <div class="flex justify-content-between flex-column sm:flex-row">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </template>

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
                </DataTable>
            </div>
        </div>
    </div>
</template>
