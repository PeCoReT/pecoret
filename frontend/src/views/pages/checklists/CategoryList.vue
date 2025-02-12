<script>
import ChecklistCategoryCreate from '@/components/dialogs/ChecklistCategoryCreate.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

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
            this.$api.get(this.$api.e.checkCategoryList, null, params).then((response) => {
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
                    this.$api.delete(this.$api.e.checkCategoryDetail, { pk: id }).then(() => {
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
            <GenericDataTable :total-records="totalRecords" :loading="loading" :pagination="pagination" blank-slate-text="No categories found!" blank-slate-title="No Categories!" blank-slate-icon="fa fa-tag" :model-value="items" @page="onPage">
                <Column field="name" header="Name">
                    <template #body="slotProps">
                        <a :href="this.$router.resolve({ name: 'ChecklistCategoryDetail', params: { categoryId: slotProps.data.pk } }).href" class="underline">{{ slotProps.data.name }}</a>
                    </template>
                </Column>
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
