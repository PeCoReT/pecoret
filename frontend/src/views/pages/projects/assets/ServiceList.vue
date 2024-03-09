<script>
import AssetService from '@/service/AssetService';
import BlankSlate from '@/components/BlankSlate.vue';
import ServiceCreateDialog from '@/components/dialogs/ServiceCreateDialog.vue';

export default {
    name: 'ServiceList',
    components: { BlankSlate, ServiceCreateDialog },
    data() {
        return {
            assetService: new AssetService(),
            projectId: this.$route.params.projectId,
            breadcrumbs: [
                {
                    label: 'Services',
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
                .getServices(this.$api, this.projectId, params)
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
                .getServices(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onSort(event) {},
        onFilter(event) {},
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: 'Do you want to delete this asset?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.assetService.deleteService(this.$api, this.projectId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Asset was deleted!',
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
    }
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
                <ServiceCreateDialog @object-created="getItems"></ServiceCreateDialog>
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
                        <BlankSlate icon="fa fa-network-wired" text="No services found!" title="No services!"></BlankSlate>
                    </template>

                    <Column field="name" header="Name">
                        <template #body="slotProps">
                            <router-link class="text-color underline" :to="{ name: 'ServiceDetail', params: { projectId: this.projectId, assetId: slotProps.data.pk } }"> {{ slotProps.data.name }}</router-link>
                        </template>
                    </Column>
                    <Column field="port" header="Port"></Column>
                    <Column field="protocol" header="Protocol"></Column>
                    <Column field="state" header="State"></Column>
                    <Column field="host.name" header="Host"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"> </Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>