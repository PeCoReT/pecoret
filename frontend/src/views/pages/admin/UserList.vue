<script>
import AdminService from '@/service/AdminService';
import UserCreateDialog from '@/components/dialogs/UserCreateDialog.vue';
import UserUpdateDialog from '@/components/dialogs/UserUpdateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'UserList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Users',
                    disabled: true
                }
            ],
            service: new AdminService(),
            loading: false,
            pagination: { page: 1, limit: 20 },
            totalRecords: 0,
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
            this.loading = true;
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.$api
                .get(this.$api.e.userList, null, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.$api
                .get(this.$api.e.userList, null, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(userId) {
            this.$confirm.require({
                message: 'Do you want to delete this user?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.userDetail, {pk: userId}).then(() => {
                        this.$toast.add({
                            severity: 'success',
                            summary: 'Deleted',
                            detail: 'User was deleted successfully!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    },
    components: { GenericDataTable, BaseListLayout, UserCreateDialog, UserUpdateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <UserCreateDialog @object-created="getItems"></UserCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No users found!"
                blank-slate-title="No Users!"
                :model-value="items"
                blank-slate-icon="fa fa-users"
                @page="onPage"
                @search="onSearch"
                :show-search="true"
                :show-refresh-button="true"
                @refresh="getItems"
            >
                <Column field="username" header="Username"></Column>
                <Column field="first_name" header="First Name"></Column>
                <Column field="last_name" header="Last Name"></Column>
                <Column field="email" header="E-Mail"></Column>
                <Column field="is_active" header="Is Active?"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <UserUpdateDialog :user="slotProps.data"></UserUpdateDialog>
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
