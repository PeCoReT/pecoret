<script>
import CompanyTabMenu from '@/components/pages/CompanyTabMenu.vue';
import CompanyService from '@/service/CompanyService';
import ContactCreateDialog from '../../../components/dialogs/ContactCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import CompanyContactUpdateDialog from "@/components/dialogs/CompanyContactUpdateDialog.vue";

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
            companyService: new CompanyService(),
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
            this.companyService
                .getContacts(this.companyId, data)
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
                    this.companyService.deleteContact(this.$api, this.companyId, id).then(() => {
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
                <ContactCreateDialog @object-created="getContacts"></ContactCreateDialog>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <CompanyTabMenu class="surface-card"></CompanyTabMenu>
            <div class="card border-noround-top">
                <div class="col-12">
                    <DataTable
                        :paginator="true"
                        dataKey="pk"
                        :rowHover="items.length > 0"
                        :rows="pagination.limit"
                        :value="items"
                        filterDisplay="menu"
                        :lazy="true"
                        responsiveLayout="scroll"
                        :totalRecords="totalRecords"
                        :loading="loading"
                        @page="onPage"
                        @sort="onSort"
                        @filter="onFilter"
                    >
                        <template #empty>
                            <BlankSlate title="No contacts!" text="No contacts found!" icon="fa fa-address-card"></BlankSlate>
                        </template>
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
                    </DataTable>
                </div>
            </div>
        </div>
    </div>
</template>