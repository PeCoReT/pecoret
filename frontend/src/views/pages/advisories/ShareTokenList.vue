<script>
import { useListViewComposable } from '@/composables/listViewComposable';
import PBreadcrumb from '@/components/Breadcrumb.vue';
import AdvisoryTabMenu from '@/components/navigation/AdvisoryTabMenu.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ShareTokenCreateDialog from '@/components/dialogs/advisories/ShareTokenCreateDialog.vue';

export default {
    name: 'ShareTokenList',
    components: { ShareTokenCreateDialog, GenericDataTable, AdvisoryTabMenu, PBreadcrumb },
    setup() {
        const { sort, buildParams } = useListViewComposable();
        return { sort, buildParams };
    },
    data() {
        return {
            loading: false,
            items: [],
            advisoryId: this.$route.params.advisoryId,
            totalRecords: 0,
            pagination: { page: 1, limit: 25 },
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Detail',
                    to: this.$router.resolve({
                        name: 'AdvisoryDetail',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                }
            ]
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        copyToClipboard(data) {
            navigator.clipboard.writeText(data);
            this.$toast.add({
                severity: 'info',
                summary: 'Copied',
                detail: 'URL copied to clipboard!',
                life: 3000
            });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getItems(params) {
            this.loading = true;
            params = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.aShareTokenList, { aPk: this.advisoryId }, params)
                .then((resp) => {
                    this.items = resp.data.results;
                    this.totalRecords = resp.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this token?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.aShareTokenDetail, { aPk: this.advisoryId, pk: id }).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Token was removed!',
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
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <p-breadcrumb :model-value="breadcrumbs"></p-breadcrumb>
        </div>
    </div>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-6"></div>
        <div class="col-span-6">
            <div class="flex justify-end">
                <ShareTokenCreateDialog @object-created="getItems"></ShareTokenCreateDialog>
            </div>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <AdvisoryTabMenu></AdvisoryTabMenu>
            <div class="card">
                <GenericDataTable
                    :total-records="totalRecords"
                    :loading="loading"
                    :pagination="pagination"
                    @page="onPage"
                    blank-slate-text="No share tokens found!"
                    blank-slate-title="No Share Tokens"
                    blank-slate-icon="fa fa-share"
                    :model-value="items"
                    :show-search="true"
                    @search="
                        (query) => {
                            this.getItems({ search: query });
                        }
                    "
                >
                    <Column field="name" header="Name"></Column>
                    <Column field="date_expire" header="Date Expire"></Column>
                    <Column field="date_created" header="Date Created"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-copy" @click="copyToClipboard(slotProps.data.url)"></Button>
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </GenericDataTable>
            </div>
        </div>
    </div>
</template>
