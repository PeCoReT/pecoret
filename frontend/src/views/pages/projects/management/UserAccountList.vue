<script>
import { UserAccountUpdateDialog } from '@/partials/projects';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Button } from '@/components/ui/button';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'UserAccountList',
    mixins: [listViewMixin],
    data() {
        return {
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            filters: {
                search: { value: null }
            }
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        commonSortFilter() {
            return commonSortFilter;
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pAccountList, { projectPk: this.projectId }, data)
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
                accept: () => {
                    this.deleteAccount(id);
                }
            });
        },
        deleteAccount(id) {
            this.$api.delete(this.$api.e.pAccountDetail, { projectPk: this.projectId, pk: id }).then(() => {
                this.$toaster({
                    title: 'Deleted',
                    description: 'Account removed from project!',
                    duration: 3000
                });
                this.getItems();
            });
        },
        copyToClipboard(password) {
            navigator.clipboard.writeText(password);
            this.$toaster({
                title: 'Copied',
                description: 'Password copied to clipboard',
                duration: 3000
            });
        }
    },
    components: {
        Paginator,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        DataViewListLayout,
        UserAccountUpdateDialog,
        Button
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>
        <template #create-button>
            <Button :href="this.$router.resolve({ name: 'UserAccountCreate', params: { projectId: this.projectId } }).href" as="a"><i class="fa fa-plus"></i> Account </Button>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <SortListDropdownMenu :items="commonSortFilter()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-users" blank-slate-text="No user accounts found!" blank-slate-title="No User Accounts!">
            <template #item="{ item }">
                <i v-if="item.compromised === true" class="fa fa-check h-4 w-4 text-primary"></i>
                <i v-else class="fa fa-xmark-circle h-4 w-4 text-secondary"></i>
                <div class="flex-1">
                    {{ item.username }}
                    <span v-if="item.description" class="flex text-muted-foreground">{{ item.description }}</span>
                </div>
                <span>Role: {{ item.role }}</span>
                <div class="flex">
                    <Button @click="copyToClipboard(item.password)" variant="outline"><i class="fa fa-clipboard"></i> </Button>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
