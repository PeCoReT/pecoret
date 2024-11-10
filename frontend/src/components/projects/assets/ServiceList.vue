<script>
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ServiceCreateDialog from '@/components/projects/assets/ServiceCreateDialog.vue';
import ServiceUpdateDialog from '@/components/projects/assets/ServiceUpdateDialog.vue';

export default {
    name: 'ServiceList',
    components: { ServiceUpdateDialog, ServiceCreateDialog, GenericDataTable },
    props: {
        hostId: {
            required: true
        },
        projectId: {
            required: true
        }
    },
    data() {
        return {
            items: [],
            totalRecords: 0,
            loading: false,
            pagination: { page: 1, limit: 20 },
            selectedItems: [],
            deleteButtonLoading: false
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                host: this.hostId,
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.$api
                .get(this.$api.e.pServiceList, { projectPk: this.projectId }, params)
                .then((resp) => {
                    this.items = resp.data.results;
                    this.totalRecords = resp.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        bulkDeleteConfirm() {
            this.$confirm.require({
                message: 'Do you want to delete all selected items?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteButtonLoading = true;
                    this.loading = true;
                    let itemsDeleted = 0;
                    this.selectedItems.forEach((item) => {
                        this.$api
                            .delete(this.$api.e.pServiceDetail, {
                                projectPk: this.projectId,
                                pk: item.pk
                            })
                            .then(() => {
                                itemsDeleted++;
                                if (itemsDeleted === this.selectedItems.length) {
                                    this.loading = false;
                                    this.deleteButtonLoading = false;
                                    this.selectedItems = [];
                                    this.getItems();
                                }
                            });
                    });
                }
            });
        },
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query,
                host: this.hostId
            };
            this.$api
                .get(this.$api.e.pServiceList, { projectPk: this.projectId }, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <div class="grid mt-3 grid-cols-1">
        <div class="col-span-1">
            <div class="card">
                <h4>Services</h4>
                <GenericDataTable
                    :total-records="totalRecords"
                    :loading="loading"
                    :pagination="pagination"
                    blank-slate-text="No services found!"
                    blank-slate-title="No Services!"
                    blank-slate-icon="fa fa-network-wired"
                    v-model:selection="selectedItems"
                    :model-value="items"
                    @page="onPage"
                    :show-search="true"
                    @search="onGlobalSearch"
                >
                    <template #header>
                        <div class="grid grid-cols-2">
                            <div class="col-span-1 justify-start flex">
                                <IconField iconPosition="left">
                                    <InputIcon class="fa fa-search"></InputIcon>
                                    <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                                </IconField>
                                <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2" :loading="deleteButtonLoading"></Button>
                            </div>
                            <div class="flex justify-end col-span-1">
                                <ServiceCreateDialog :host-id="this.hostId" :project-id="this.projectId" @object-created="getItems"></ServiceCreateDialog>
                            </div>
                        </div>
                    </template>
                    <Column selectionMode="multiple" headerStyle=""></Column>

                    <Column field="name" header="Name"></Column>
                    <Column field="port" header="Port"></Column>
                    <Column field="protocol" header="Protocol"></Column>
                    <Column field="state" header="State"></Column>
                    <Column field="product" header="Product"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <ServiceUpdateDialog :asset="slotProps.data" @object-updated="getItems"></ServiceUpdateDialog>
                        </template>
                    </Column>
                </GenericDataTable>
            </div>
        </div>
    </div>
</template>
