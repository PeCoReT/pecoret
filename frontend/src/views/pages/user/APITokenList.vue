<script>
import { useAuthStore } from '@/store/auth';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import { Button } from '@/components/ui/button';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Alert } from '@/components/alert';
import UserSettingsPageLayout from '@/layout/UserSettingsPageLayout.vue';
import { Paginator } from '@/components/paginator';

export default {
    name: 'APITokenList',
    components: {
        Paginator,
        UserSettingsPageLayout,
        Alert,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        DataViewListLayout,
        Button
    },
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
            pagination: { page: 1, limit: 20 },
            authStore: useAuthStore(),
            selection: {},
            filters: {
                search: { value: null }
            }
        };
    },
    methods: {
        commonSortFilter() {
            return commonSortFilter;
        },
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
        copyToClipboard() {
            navigator.clipboard.writeText(this.authStore.newApiToken);
            this.$toaster({
                title: 'Copied',
                description: 'Token copied to clipboard!',
                duration: 3000
            });
        },
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.$api
                .get(this.$api.e.apiTokenList, null, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        async bulkDelete() {
            this.$confirm.require({
                accept: async () => {
                    let itemsDeleted = 0;
                    let totalLength = Object.entries(this.selection).length;
                    for (const [key, value] of Object.entries(this.selection)) {
                        itemsDeleted++;
                        if (value === true) {
                            await this.$api
                                .delete(this.$api.e.apiTokenDetail, {
                                    pk: key
                                })
                                .then(() => {
                                    if (itemsDeleted === totalLength) {
                                        this.selection = {};
                                        this.getItems();
                                    }
                                });
                        }
                    }
                }
            });
        }
    },
    mounted() {
        this.getItems();
    },
    beforeUnmount() {
        this.authStore.setNewApiToken(null);
    }
};
</script>
<template>
    <UserSettingsPageLayout subheadline="Manage your API tokens!" headline="API Tokens">
        <div class="pt-6 pb-6">
            <div class="col-span-12">
                <div class="flex justify-between items-center w-full">
                    <div class="flex-1 pr-2">
                        <SearchField v-model="filters.search.value" @search="onGlobalSearch"></SearchField>
                    </div>
                    <div class="flex-shrink-0">
                        <Button :href="this.$router.resolve({ name: 'APITokenCreate' }).href" as="a"><i
                                class="fa fa-plus"></i>
                            API-Token
                        </Button>
                    </div>
                </div>
            </div>

            <Alert v-if="authStore.newApiToken" class="mt-3" message="">
                <p><strong>API-Token: </strong>{{ authStore.newApiToken }}</p>
                <Button class="hover:border" variant="icon" @click="copyToClipboard"><i class="fa fa-clipboard"></i>
                </Button>
            </Alert>

            <div class="py-4">
                <DataViewHeader :total-records="totalRecords" :items="items" :show-bulk-select="true"
                    v-model:selection="selection">
                    <template #filters>
                        <SortListDropdownMenu :items="commonSortFilter()"></SortListDropdownMenu>
                    </template>
                    <template #bulk>
                        <Button @click="bulkDelete" variant="destructive"><i class="fa fa-trash" /> Delete</Button>
                    </template>
                </DataViewHeader>
                <DataViewContent blank-slate-icon="fa fa-key" blank-slate-text="No API tokens found!"
                    blank-slate-title="No API Tokens!" :items="items" :loading="loading" :show-bulk-select="true"
                    v-model:selection="selection">
                    <template #item="{ item }">
                        <div class="flex-1">
                            {{ item.name }}
                            <div class="flex">
                                <span class="text-sm text-muted-foreground">Prefix: {{ item.prefix }}</span>
                                <span class="mx-2">|</span>
                                <span class="text-sm text-muted-foreground">Created: {{ item.date_created }}</span>
                            </div>
                            <div class="flex text-xs text-muted-foreground">
                                <span>Expiry: {{ item.date_expire || 'Never' }}</span>
                            </div>
                        </div>
                        <span>{{ item.date_last_used || 'Never used' }}</span>
                    </template>
                </DataViewContent>
                <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
                    class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
            </div>
        </div>
    </UserSettingsPageLayout>
</template>
