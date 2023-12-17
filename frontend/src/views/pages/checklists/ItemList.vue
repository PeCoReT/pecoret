<script>
import ChecklistService from '@/service/ChecklistService';
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'ItemList',
    components: { BlankSlate },
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
                    label: 'Items',
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
                this.totalRecords = response.data.counts;
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
        }
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
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <Button outlined @click="this.$router.push({ name: 'ChecklistCreate' })" icon="fa fa-plus" label="Checklist"></Button>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable :paginator="true" dataKey="pk" :rowHover="items.length > 0" :rows="pagination.limit" :value="items" filterDisplay="menu" :lazy="true" :loading="loading" @page="onPage" :totalRecords="totalRecords">
                    <Column field="category_id" header="Category ID"></Column>
                    <Column field="name" header="Name"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                    <template #empty>
                        <BlankSlate icon="fa fa-tag" title="No Categories!" text="No Categories found!"></BlankSlate>
                    </template>
                </DataTable>
            </div>
        </div>
    </div>
</template>