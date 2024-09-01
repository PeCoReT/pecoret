<script>
import UserAccountService from '@/service/UserAccountService';
import UserAccountCreateDialog from '@/components/dialogs/UserAccountCreateDialog.vue';
import UserAccountUpdateDialog from '@/components/dialogs/UserAccountUpdateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'UserAccountList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'User Accounts',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            service: new UserAccountService()
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
            this.service
                .getAccounts(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to delete this account?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteAccount(id);
                }
            });
        },
        deleteAccount(id) {
            this.service.deleteAccount(this.$api, this.projectId, id).then(() => {
                this.$toast.add({
                    severity: 'info',
                    summary: 'Deleted',
                    detail: 'Account removed from project!',
                    life: 3000
                });
                this.getItems();
            });
        },
        copyToClipboard(password) {
            navigator.clipboard.writeText(password);
            this.$toast.add({
                severity: 'info',
                summary: 'Copied',
                detail: 'Password copied to clipboard',
                life: 3000
            });
        }
    },
    components: { GenericDataTable, BaseListLayout, UserAccountCreateDialog, UserAccountUpdateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <UserAccountCreateDialog @object-created="getItems"></UserAccountCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No user accounts found!"
                blank-slate-title="No User Accounts!"
                blank-slate-icon="fa fa-users"
                :model-value="items"
                @page="onPage"
            >
                <Column field="username" header="Username"></Column>
                <Column field="password" header="Password">
                    <template #body=""> ***</template>
                </Column>
                <Column field="role" header="Role"></Column>
                <Column field="description" header="Description"></Column>
                <Column field="compromised" header="Compromised"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-copy" @click="copyToClipboard(slotProps.data.password)"></Button>
                        <UserAccountUpdateDialog :account="slotProps.data" @object-updated="this.getItems"></UserAccountUpdateDialog>
                        <Button size="small" outlined severity="danger" icon="fa fa-trash" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
