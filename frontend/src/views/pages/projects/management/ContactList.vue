<script>
import ProjectContactCreateDialog from '@/components/dialogs/ProjectContactCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'ContactList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Contacts',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
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
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            let url = this.$api.e.projectsContactList;
            this.$api
                .get(url, { projectPk: this.projectId }, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(contactId) {
            this.$confirm.require({
                message: 'Do you want to delete this contact?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteContact(contactId);
                }
            });
        },
        deleteContact(contactId) {
            this.$api.delete(this.$api.e.projectsContactDetail, { projectPk: this.projectId, pk: contactId }).then(() => {
                this.$toast.add({
                    severity: 'info',
                    summary: 'Contact Removed!',
                    detail: 'Removed contact from project!',
                    life: 3000
                });
                this.getItems();
            });
        }
    },
    components: { GenericDataTable, BaseListLayout, ProjectContactCreateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ProjectContactCreateDialog @object-created="getItems"></ProjectContactCreateDialog>
        </template>
        <template #table>
            <GenericDataTable :total-records="totalRecords" :loading="loading" :pagination="pagination" blank-slate-text="No contacts found!" blank-slate-title="No Contacts!" blank-slate-icon="fa fa-id-card" :model-value="items" @page="onPage">
                <Column field="name" header="Name">
                    <template #body="slotProps">
                        {{ slotProps.data.contact.first_name }}
                        {{ slotProps.data.contact.last_name }}
                    </template>
                </Column>
                <Column field="contact.email" header="E-Mail"></Column>
                <Column field="contact.phone" header="Phone"></Column>
                <Column field="contact.role" header="Role"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined severity="danger" icon="fa fa-trash" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
