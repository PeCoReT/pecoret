<script>
import CompanyTabMenu from '@/components/navigation/CompanyTabMenu.vue';
import ContactCreateDialog from '@/components/dialogs/ContactCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import CompanyContactUpdateDialog from '@/components/dialogs/CompanyContactUpdateDialog.vue';

export default {
    name: 'CompanyContactList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Companies',
                    to: this.$router.resolve({
                        name: 'CompanyList'
                    })
                },
                {
                    label: 'Company Details',
                    to: this.$router.resolve({
                        name: 'CompanyDetail',
                        params: {
                            companyId: this.$route.params.companyId
                        }
                    })
                },
                {
                    label: 'Contacts',
                    disabled: true
                }
            ],
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            companyId: this.$route.params.companyId
        };
    },
    mounted() {
        this.getContacts();
    },
    methods: {
        getContacts() {
            this.loading = true;
            let data = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.$api
                .get(this.$api.e.cContactList, { cPk: this.companyId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onFilter() {},
        onSort() {},
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getContacts();
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to delete this contact?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.cContactDetail, { cPk: this.companyId, pk: id }).then(() => {
                        this.getContacts();
                    });
                }
            });
        }
    },
    components: { CompanyContactUpdateDialog, BlankSlate, CompanyTabMenu, ContactCreateDialog }
};
</script>

<template>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid grid-col-12 mt-3">
        <div class="col-span-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-span-6">
            <div class="flex justify-end">
                <ContactCreateDialog @object-created="getContacts"></ContactCreateDialog>
            </div>
        </div>
    </div>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <CompanyTabMenu class="surface-card"></CompanyTabMenu>
            <div class="card border-noround-top">
                <div class="col-span-12">
                    <GenericDataTable
                        :total-records="totalRecords"
                        :loading="loading"
                        :pagination="pagination"
                        blank-slate-text="No contacts found!"
                        blank-slate-title="Not Contacts"
                        blank-slate-icon="fa fa-address-card"
                        :model-value="items"
                        @page="onPage"
                    >
                        <Column field="first_name" header="First Name"></Column>
                        <Column field="last_name" header="Last Name"></Column>
                        <Column field="email" header="E-Mail"></Column>
                        <Column field="phone" header="Phone"></Column>
                        <Column field="role" header="Role"></Column>
                        <Column header="Actions">
                            <template #body="slotProps">
                                <CompanyContactUpdateDialog :company="slotProps.data" @object-updated="this.getContacts"></CompanyContactUpdateDialog>
                                <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                            </template>
                        </Column>
                    </GenericDataTable>
                </div>
            </div>
        </div>
    </div>
</template>
