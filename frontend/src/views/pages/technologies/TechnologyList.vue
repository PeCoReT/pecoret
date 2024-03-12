<script>
import TechnologyService from '@/service/TechnologyService';
import BlankSlate from '@/components/BlankSlate.vue';
import TechnologyCreateDialog from '@/components/knowledgebase/TechnologyCreateDialog.vue';
import TechnologyUpdateDialog from '@/components/knowledgebase/TechnologyUpdateDialog.vue';

export default {
    name: 'TechnologyList',
    components: { TechnologyUpdateDialog, TechnologyCreateDialog, BlankSlate },
    data() {
        return {
            service: new TechnologyService(),
            loading: false,
            breadcrumbs: [
                {
                    label: 'Technologies',
                    disabled: true
                }
            ],
            items: [],
            totalRecords: 0,
            pagination: { page: 1, limit: 25 }
        };
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service
                .getTechnologies(this.$api, params)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onGlobalSearch(query) {
            let params = {
                search: query
            };
            this.service.getTechnologies(this.$api, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this technology?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteTechnology(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Technology was removed!',
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
                <TechnologyCreateDialog @object-created="getItems"></TechnologyCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable paginator lazy dataKey="pk" :value="items" :rows="pagination.limit" :row-hover="items.length > 0" :totalRecords="totalRecords" :loading="loading" @page="onPage">
                    <template #empty>
                        <BlankSlate title="No Technologies!" text="No technologies found!" icon="fa fa-microchip"></BlankSlate>
                    </template>
                    <template #header>
                        <div class="grid">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </template>
                    <Column field="name" header="Name"></Column>
                    <Column field="cpe" header="CPE"></Column>
                    <Column field="homepage" header="Homepage"></Column>
                    <Column field="date_updated" header="Updated"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <TechnologyUpdateDialog :technology="slotProps.data" @object-updated="getItems"></TechnologyUpdateDialog>
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>
