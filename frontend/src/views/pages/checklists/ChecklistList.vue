<script>
import ChecklistService from '@/service/ChecklistService';
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'ChecklistList',
    components: { BlankSlate },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Checklists'
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
            this.service.getChecklists(this.$api, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.counts;
            });
        },
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: 'Do you want to delete this checklist?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteChecklist(this.$api, id).then(() => {
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
                    <Column field="checklist_id" header="Checklist ID">
                        <template #body="slotProps">
                            <router-link class="text-color underline" :to="{ name: 'ChecklistUpdate', params: { checklistId: slotProps.data.pk } }">
                                {{ slotProps.data.checklist_id }}
                            </router-link>
                        </template>
                    </Column>
                    <Column field="name" header="Name"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                    <template #empty>
                        <BlankSlate icon="fa fa-check" title="No Checklists!" text="No Checklists found!"></BlankSlate>
                    </template>
                </DataTable>
            </div>
        </div>
    </div>
</template>