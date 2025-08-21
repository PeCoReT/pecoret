<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import { Button } from '@/components/ui/button';
import { Paginator } from '@/components/paginator';
import SearchField from '@/partials/common/SearchField.vue';
import ChecklistTabMenu from '@/partials/knowledgebase/ChecklistTabMenu.vue';
import { listViewMixin } from "@/mixins/listViewMixin";

export default {
    name: 'ChecklistList',
    mixins: [listViewMixin],
    components: {
        ChecklistTabMenu,
        SearchField,
        Paginator,
        SortListDropdownMenu,
        DataViewHeader,
        DataViewContent,
        DataViewListLayout,
        Button
    },
    data() {
        return {
            loading: false,
            items: [],
            filters: {
                search: { value: null },
            },
            selectedItems: [],
            deleteButtonLoading: false,
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        commonSortFilter() {
            return commonSortFilter;
        },
        async bulkDelete() {
            this.$confirm.require({
                accept: async () => {
                    let itemsDeleted = 0;
                    let totalLength = Object.entries(this.selectedItems).length;
                    for (const [key, value] of Object.entries(this.selectedItems)) {
                        itemsDeleted++;
                        if (value === true) {
                            await this.$api
                                .delete(this.$api.e.checklistDetail, {
                                    pk: key
                                })
                                .then(() => {
                                    if (itemsDeleted === totalLength) {
                                        this.selectedItems = {};
                                        this.getItems();
                                    }
                                });
                        }
                    }
                }
            });
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.checklistList, null, data)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>
<template>
    <DataViewListLayout>
        <template #pre-content>
            <ChecklistTabMenu class="md:max-w-lg mt-4"></ChecklistTabMenu>
        </template>
        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>
        <template #create-button>
            <Button :href="this.$router.resolve({ name: 'ChecklistCreate' }).href" as="a"><i class="fa fa-plus"></i>
                Checklist
            </Button>
        </template>
        <DataViewHeader v-model:items="items" :total-records="totalRecords" :show-bulk-select="true"
            v-model:selection="selectedItems">
            <template #filters>
                <SortListDropdownMenu :items="commonSortFilter()"></SortListDropdownMenu>
            </template>
            <template #bulk>
                <Button @click="bulkDelete" variant="destructive"><i class="fa fa-trash" /> Delete</Button>
            </template>
        </DataViewHeader>
        <DataViewContent blank-slate-icon="fa fa-check" blank-slate-text="No checklists found!"
            blank-slate-title="No Checklists!" v-model:selection="selectedItems" :show-bulk-select="true" :items="items"
            :loading="loading">
            <template #item="{ item }">
                <div class="flex-1">
                    <a :href="this.$router.resolve({ name: 'ChecklistUpdate', params: { checklistId: item.pk } }).href"
                        class="hover:underline">{{ item.name }}</a>
                    <div class="flex text-xs text-muted-foreground">
                        {{ item.checklist_id }}
                    </div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
