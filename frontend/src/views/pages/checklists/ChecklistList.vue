<script>
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'ChecklistList',
    components: { GenericDataTable, BaseListLayout },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Checklists'
                }
            ],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            items: []
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
        getItems() {
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.$api.get(this.$api.e.checklistList, null, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: 'Do you want to delete this checklist?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.checklistDetail, { pk: id }).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Checklist was deleted!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
    }
};
</script>
<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <Button outlined @click="this.$router.push({ name: 'ChecklistCreate' })" icon="fa fa-plus" label="Checklist"></Button>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No checklists found!"
                blank-slate-title="No Checklists!"
                blank-slate-icon="fa fa-check"
                :model-value="items"
                @page="onPage"
            >
                <Column field="name" header="Name">
                    <template #body="slotProps">
                        <a :href="this.$router.resolve({name: 'ChecklistUpdate', params: {checklistId: slotProps.data.pk}}).href" class="underline">{{ slotProps.data.name }}</a>
                    </template>
                </Column>
                <Column field="checklist_id" header="Checklist ID"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
