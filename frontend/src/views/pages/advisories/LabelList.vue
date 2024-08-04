<script>
import { defineComponent } from 'vue';
import AdvisoryService from '@/service/AdvisoryService';
import LabelCreateDialog from '@/components/advisories/LabelCreateDialog.vue';
import AdvisoryLabelBadge from '@/components/advisories/AdvisoryLabelBadge.vue';
import LabelUpdateDialog from '@/components/advisories/LabelUpdateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default defineComponent({
    name: 'LabelList',
    components: {
        GenericDataTable,
        BaseListLayout,
        LabelUpdateDialog,
        LabelCreateDialog,
        AdvisoryLabelBadge
    },
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
            breadcrumbs: [
                {
                    label: 'Labels',
                    disabled: true
                }
            ],
            items: [],
            totalRecords: 0,
            pagination: { page: 1, limit: 25 },
            filters: {}
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onGlobalSearch(query) {
            let params = {
                search: query
            };
            this.service.getLabels(this.$api, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this label?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteLabel(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Label was removed!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service
                .getLabels(this.$api, params)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
});
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <LabelCreateDialog @object-created="getItems"></LabelCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No labels found!"
                blank-slate-title="No Labels!"
                blank-slate-icon="fa fa-tags"
                :model-value="items"
                @page="onPage"
                v-model:filters="filters"
                filter-display="menu"
                :show-search="true"
                @search="onGlobalSearch"
            >
                <Column field="name" header="Name"></Column>
                <Column field="description" header="Description"></Column>
                <Column header="Preview">
                    <template #body="slotProps">
                        <AdvisoryLabelBadge :label="slotProps.data"></AdvisoryLabelBadge>
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <LabelUpdateDialog :label="slotProps.data" @object-updated="getItems"></LabelUpdateDialog>
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>

<style scoped></style>
