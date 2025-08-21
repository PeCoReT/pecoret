<script>
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { Badge } from '@/components/badge';
import { SortListDropdownMenu } from '@/components/dropdown-menu';
import SearchField from '@/partials/common/SearchField.vue';
import { DataViewHeader } from '@/components/dataview';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import ScopeBadge from '@/partials/common/ScopeBadge.vue';
import { commonSortFilter } from '@/utils/constants';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';
import { paramMixin } from '@/mixins/params';
import RadioDropdownMenu from '@/components/dropdown-menu/RadioDropdownMenu.vue';
import { ModelCombobox } from '@/components/combobox';
import TechnologyBadge from '@/partials/knowledgebase/TechnologyBadge.vue';

export default {
    name: 'URLList',
    mixins: [listViewMixin, paramMixin],
    components: {
        TechnologyBadge,
        ModelCombobox,
        RadioDropdownMenu,
        Paginator,
        ScopeBadge,
        DataViewContent,
        DataViewListLayout,
        DataViewHeader,
        SearchField,
        SortListDropdownMenu,
        DefaultSkeleton,
        Badge
    },
    data() {
        return {
            items: [],
            loading: false,
            pagination: { limit: 25, page: 1 },
            totalRecords: 0,
            programs: [],
            filters: {
                technologies: { value: null },
                ordering: { value: '-date_created' },
                program: { value: null },
                search: { value: null }
            },
            urlSortItems: commonSortFilter
        };
    },
    mounted() {
        this.initFromUrl();
        this.getItems();
    },
    methods: {
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asUrlList, null, data)
                .then((resp) => {
                    this.items = resp.data.results;
                    this.totalRecords = resp.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(page) {
            this.pagination.page = page;
            this.getItems();
        }
    }
};
</script>

<template>
    <DataViewListLayout :search-full-width="true">
        <template #search>
            <SearchField v-model="filters.search.value" @update:modelValue="getItems()"></SearchField>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <ModelCombobox v-model="this.filters.technologies.value" :api-endpoint="this.$api.e.technologyList" label="Technologies" @select="this.getItems()" :fluid="true"></ModelCombobox>

                <SortListDropdownMenu :items="urlSortItems" v-model="filters.ordering.value" @update:model-value="getItems()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-sitemap" blank-slate-text="No urls here!" blank-slate-title="No URLs!">
            <template #item="{ item }">
                <div class="flex-1">
                    <div class="flex justify-between items-center">
                        <a :href="this.$router.resolve({ name: 'AttackSurfaceURLDetail', params: { urlId: item.pk } }).href" class="font-semibold text-base hover:underline">{{ item.url }}</a>
                        <!-- In Scope & Project Name -->
                        <div class="flex items-center space-x-4 text-sm">
                            <span class="font-normal">{{ item.service.target.program.name }}</span>

                            <Badge v-if="item.is_in_scope === true" color="#66BB6A" text="In Scope"></Badge>
                            <Badge v-else color="#cbcbcb" text="Out of Scope"></Badge>
                        </div>
                    </div>

                    <div class="flex flex-wrap gap-2">
                        <TechnologyBadge :key="technology.pk" v-for="technology in item.technologies" :technology="technology"> </TechnologyBadge>
                    </div>

                    <div class="text-xs text-gray-500 mt-2">
                        <span>
                            Created: <span class="font-medium">{{ item.date_created }}</span>
                        </span>
                        <span class="mx-2">|</span>
                        <span>
                            Updated: <span class="font-medium">{{ item.date_updated }}</span>
                        </span>
                        <span v-if="item.status_code" class="mx-2">|</span>
                        <span v-if="item.status_code">
                            Status code: <span class="font-medium">{{ item.status_code }}</span>
                        </span>
                    </div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
