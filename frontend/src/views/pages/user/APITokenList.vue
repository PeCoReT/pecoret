<script>
import APITokenCreate from '@/components/dialogs/APITokenCreate.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';

export default {
    name: 'APITokenList',
    components: { GenericDataTable, BaseListLayout, APITokenCreate },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'API-Tokens',
                    disabled: true
                }
            ],
            tokenKey: null,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 }
        };
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
            this.$api.get(this.$api.e.apiTokenList, null, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        showTokenKey(data) {
            this.tokenKey = data.token;
            this.getItems();
        },
        copyToClipboard() {
            navigator.clipboard.writeText(this.tokenKey);
            this.$toast.add({
                severity: 'info',
                summary: 'Copied',
                detail: 'Token copied to clipboard!',
                life: 3000
            });
        },
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.$api.get(this.$api.e.apiTokenList, null, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: 'Do you want to delete this api token?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.apiTokenDetail, {pk: id}).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'API Token was deleted!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    },
    mounted() {
        this.getItems();
    }
};
</script>
<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <APITokenCreate @object-created="showTokenKey"></APITokenCreate>
        </template>

        <template #table>
            <div class="grid" v-if="tokenKey">
                <div class="col-12">
                    <Message
                        @close="
                            () => {
                                this.tokenKey = null;
                            }
                        "
                    >
                        <div class="row">
                            <div class="col">
                                {{ tokenKey }}

                                <Button class="ml-5 p-0" icon="fa fa-copy" outlined @click="copyToClipboard"></Button>
                            </div>
                        </div>
                    </Message>
                </div>
            </div>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No API-Tokens found!"
                blank-slate-title="No API-Tokens!"
                blank-slate-icon="fa fa-fingerprint"
                :model-value="items"
                @search="onGlobalSearch"
                @page="onPage"
                :show-search="true"
            >
                <Column field="name" header="Name"></Column>
                <Column field="prefix" header="Prefix"></Column>
                <Column field="date_last_used" header="Last used"></Column>
                <Column field="date_created" header="Date created"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="onDeleteConfirmDialog(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
