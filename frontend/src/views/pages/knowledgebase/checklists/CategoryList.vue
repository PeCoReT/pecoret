<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import ChecklistTabMenu from '@/partials/knowledgebase/ChecklistTabMenu.vue';
import { Paginator } from '@/components/paginator';
import { Button } from '@/components/ui/button';
import { listViewMixin } from "@/mixins/listViewMixin";

export default {
    name: 'CategoryList',
    components: {
        Paginator,
        Button,
        ChecklistTabMenu,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        DataViewListLayout
    },
    mixins: [listViewMixin],
    data() {
        return {
            loading: false,
            items: [],
            filters: {
                search: { value: null },
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
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api.get(this.$api.e.checkCategoryList, null, data).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
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
            <Button as="a" :href="this.$router.resolve({ name: 'ChecklistCategoryCreate' }).href"><i
                    class="fa fa-plus"></i> Category </Button>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <SortListDropdownMenu :items="commonSortFilter()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-th"
            blank-slate-text="No categories found!" blank-slate-title="No Categories!">
            <template #item="{ item }">
                <div class="flex-1">
                    <a :href="this.$router.resolve({ name: 'ChecklistCategoryUpdate', params: { categoryId: item.pk } }).href"
                        class="hover:underline">{{ item.name }}</a>
                    <div class="flex text-xs text-muted-foreground">
                        {{ item.category_id }}
                    </div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
