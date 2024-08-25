<script>
import ContributorService from '@/service/ContributorService';
import ContributorCreateDialog from '@/components/dialogs/ContributorCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'ContributorList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Team',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            contributorService: new ContributorService()
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
        onSearch(search) {
          this.getItems({search: search})
        },
        getItems(params) {
            this.loading = true;
            if (!params) {
                params = {};
            }
            params = {
                ...params,
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.contributorService
                .getContributors(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(contribId) {
            this.$confirm.require({
                message: 'Do you want to delete this member?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteContributor(contribId);
                }
            });
        },
        deleteContributor(contribId) {
            this.contributorService.deleteContributor(this.$api, this.projectId, contribId).then(() => {
                this.$toast.add({
                    severity: 'info',
                    summary: 'Deleted',
                    detail: 'Member removed from project!',
                    life: 3000
                });
                this.getItems();
            });
        }
    },
    components: { GenericDataTable, BaseListLayout, ContributorCreateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ContributorCreateDialog @object-created="getItems"></ContributorCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No Contributors!"
                blank-slate-title="No contributors found!"
                blank-slate-icon="fa fa-users"
                :model-value="items"
                @page="onPage"
                :show-search="true"
                @search="onSearch"
            >
                <Column field="user.username" header="User"></Column>
                <Column field="role" header="Role"></Column>
                <Column field="active_until" header="Membership Expiry">
                    <template #body="slotProps">
                        {{ slotProps.data.active_until || 'Never' }}
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined severity="danger" icon="fa fa-trash" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
