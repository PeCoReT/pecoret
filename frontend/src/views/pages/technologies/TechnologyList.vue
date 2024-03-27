<script>
import TechnologyService from '@/service/TechnologyService';
import TechnologyCreateDialog from '@/components/knowledgebase/TechnologyCreateDialog.vue';
import TechnologyUpdateDialog from '@/components/knowledgebase/TechnologyUpdateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'TechnologyList',
    components: { GenericDataTable, BaseListLayout, TechnologyUpdateDialog, TechnologyCreateDialog },
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
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <TechnologyCreateDialog @object-created="getItems"></TechnologyCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No technologies found!"
                blank-slate-title="No Technologies!"
                blank-slate-icon="fa fa-microship"
                :model-value="items"
                @page="onPage"
                :show-search="true"
                @search="onGlobalSearch"
            >
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
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
