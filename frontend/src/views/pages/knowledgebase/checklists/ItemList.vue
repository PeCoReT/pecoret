<script>
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Button } from '@/components/ui/button';
import ChecklistTabMenu from '@/partials/knowledgebase/ChecklistTabMenu.vue';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'ChecklistItemList',
    mixins: [listViewMixin],
    components: {
        Paginator,
        SortListDropdownMenu,
        SearchField,
        DataViewListLayout,
        ChecklistTabMenu,
        DataViewContent,
        DataViewHeader,
        Button
    },
    mounted() {
        this.getItems();
    },
    data() {
        return {
            items: [],
            loading: false,
            filters: {
                search: { value: null }
            }
        };
    },
    methods: {
        commonSortFilter() {
            return commonSortFilter;
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.checkItemList, null, data)
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
            <SearchField v-model="filters.search.value" @search="getItems()"></SearchField>
        </template>
        <template #create-button>
            <Button as="a" :href="this.$router.resolve({ name: 'ChecklistItemCreate' }).href"><i class="fa fa-plus"></i>
                Item
            </Button>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <SortListDropdownMenu :items="commonSortFilter()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent v-model:items="items" :loading="loading" blank-slate-text="No items found!"
            blank-slate-icon="fa fa-cube" blank-slate-title="No Items!">
            <template #item="{ item }">
                <div class="flex-1">
                    <a :href="this.$router.resolve({ name: 'ChecklistItemUpdate', params: { itemId: item.pk } }).href"
                        class="hover:underline">{{ item.name }}</a>
                    <div class="flex text-xs text-muted-foreground">
                        <span> Created: {{ item.date_created }} </span>
                        <span class="mx-2">|</span>
                        <span> Updated: {{ item.date_updated }} </span>
                    </div>
                </div>
                <span class="flex text-muted-foreground">
                    {{ item.category.category_id }}
                </span>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
