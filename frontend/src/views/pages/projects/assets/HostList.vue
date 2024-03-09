<script>
import AssetService from '@/service/AssetService';
import HostCreateDialog from '@/components/dialogs/HostCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'HostList',
    data() {
        return {
            assetService: new AssetService(),
            projectId: this.$route.params.projectId,
            breadcrumbs: [
                {
                    label: 'Hosts',
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
                .getHosts(this.$api, this.projectId, params)
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
                .getHosts(this.$api, this.projectId, params)
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
                message: 'Do you want to delete this host?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.assetService.deleteHost(this.$api, this.projectId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Host was deleted!',
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
    components: { HostCreateDialog, BlankSlate }
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
                <HostCreateDialog @object-created="getItems"></HostCreateDialog>
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
                        <BlankSlate icon="fa fa-server" title="No hosts!" text="No hosts found!"></BlankSlate>
                    </template>

                    <Column field="ip" header="IP">
                        <template #body="slotProps">
                            <router-link class="text-color underline" :to="{ name: 'HostDetail', params: { projectId: this.projectId, assetId: slotProps.data.pk } }">
                                {{ slotProps.data.ip }}
                            </router-link>
                        </template>
                    </Column>
                    <Column field="dns" header="DNS"></Column>
                    <Column field="operating_system" header="Operating System"></Column>
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
