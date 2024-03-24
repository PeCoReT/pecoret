<script>
import ChecklistService from '@/service/ChecklistService';
import ChecklistCategoryCreate from '@/components/dialogs/ChecklistCategoryCreate.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'CategoryList',
    components: { GenericDataTable, BaseListLayout, ChecklistCategoryCreate },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Checklists',
                    to: this.$router.resolve({
                        name: 'ChecklistList'
                    })
                },
                {
                    label: 'Categories',
                    disabled: true
                }
            ],
            loading: false,
            service: new ChecklistService(),
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
            this.service.getCategories(this.$api, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: 'Do you want to delete this category?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteCategory(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Category was deleted!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
        onRowClick(row) {
            this.$router.push({
                name: 'ChecklistCategoryDetail',
                params: {
                    categoryId: row.data.pk
                }
            });
        }
    }
};
</script>
<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ChecklistCategoryCreate @object-created="getItems"></ChecklistCategoryCreate>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No categories found!"
                blank-slate-title="No Categories!"
                blank-slate-icon="fa fa-tag"
                :model-value="items"
                @page="onPage"
                @rowClick="onRowClick"
            >
                <Column field="name" header="Name"></Column>
                <Column field="category_id" header="Category ID"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
