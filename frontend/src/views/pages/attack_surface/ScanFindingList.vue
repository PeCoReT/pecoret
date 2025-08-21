<script>
import { Badge } from '@/components/badge';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { SeverityDropdownMenu, SortListDropdownMenu } from '@/components/dropdown-menu';
import SearchField from '@/partials/common/SearchField.vue';
import BlankSlate from '@/components/blankslate/BlankSlate.vue';
import { DataViewContent, DataViewHeader } from '@/components/dataview';
import RadioDropdownMenu from '@/components/dropdown-menu/RadioDropdownMenu.vue';
import { asFindingStatusChoices, commonSortFilter } from '@/utils/constants';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import { Paginator } from '@/components/paginator';
import { Select } from '@/components/select';
import { listViewMixin } from '@/mixins/listViewMixin';
import { paramMixin } from '@/mixins/params';

export default {
    name: 'ScanFindingList',
    components: {
        Select,
        DataViewListLayout,
        RadioDropdownMenu,
        DataViewHeader,
        DataViewContent,
        SeverityDropdownMenu,
        BlankSlate,
        SearchField,
        SortListDropdownMenu,
        DefaultSkeleton,
        Badge,
        Paginator
    },
    mixins: [listViewMixin, paramMixin],
    data() {
        return {
            items: [],
            loading: false,
            sortItems: commonSortFilter,
            selection: {},
            filters: {
                status: { value: 'Open' },
                severity: { value: '' },
                search: { value: null },
                ordering: { value: '-date_created' }
            }
        };
    },
    methods: {
        asFindingStatusChoices() {
            return asFindingStatusChoices;
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asScanFindingList, null, data)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        async bulkPatch(data) {
            for (const [key, value] of Object.entries(this.selection)) {
                if (value === true) {
                    await this.$api.patch(this.$api.e.asScanFindingDetail, { pk: key }, data);
                }
            }
            this.selection = {};
            this.getItems();
        },
    },
    mounted() {
        this.getItems();
    }
};
</script>

<template>
    <DataViewListLayout :search-full-width="true">
        <template #search>
            <SearchField v-model="filters.search.value" @search="getItems()"></SearchField>
        </template>
        <DataViewHeader :total-records="totalRecords" :show-bulk-select="true" v-model:selection="selection"
            v-model:items="items">
            <template #filters>
                <RadioDropdownMenu v-model="filters.status.value" :items="[
                    { label: 'Open', value: 'Open' },
                    { label: 'Closed', value: 'Closed' }
                ]" label="Status" @select="getItems()"></RadioDropdownMenu>
                <SeverityDropdownMenu v-model="filters.severity.value" @select="this.getItems()"></SeverityDropdownMenu>
                <SortListDropdownMenu :items="sortItems" v-model="filters.ordering.value"
                    @update:model-value="this.getItems()"></SortListDropdownMenu>
            </template>
            <template #bulk>
                <Select :options="asFindingStatusChoices()" placeholder="Status" @update:model-value="
                    (value) => {
                        this.bulkPatch({ status: value });
                    }
                "></Select>
            </template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" v-model:selection="selection" :show-bulk-select="true">
            <template #blankslate>
                <BlankSlate v-if="items.length < 1" class="border rounded-t-none rounded-b-lg" icon="fa fa-bugs"
                    text="No scan findings here!" title="No Scan Findings!"></BlankSlate>
            </template>
            <template #item="{ item }">
                <div class="flex-1">
                    <div class="flex justify-between items-center mb-1">
                        <div class="font-semibold text-base items-center flex">
                            <a :href="this.$router.resolve({ name: 'AttackSurfaceScanFindingDetail', params: { findingId: item.pk } }).href"
                                class="hover:underline">
                                {{ item.name }}
                            </a>
                            <Badge v-if="item.severity" :text="item.severity" :variant="item.severity" class="ml-5">
                            </Badge>
                        </div>
                    </div>

                    <div class="flex flex-wrap">
                        <span v-for="tag in item.tags" :key="tag.pk"
                            class="bg-background text-accent-foreground text-sm px-2 py-1 rounded border border-gray-800 hover:bg-surface-800 hover:cursor-pointer">
                            {{ tag.name }}
                        </span>
                    </div>
                    <div class="text-xs text-muted-foreground">
                        <span>
                            Created: <span>{{ item.date_created }}</span>
                        </span>
                        <span class="mx-2">|</span>
                        <span> Updated: {{ item.date_updated }} </span>
                        <span class="mx-2">|</span>
                        <span>{{ item.affected_component }}</span>
                    </div>
                </div>
                <div class="flex-1"></div>
                <div class="flex">
                    <div class="flex items-center space-x-4 text-sm">
                        <Badge :text="item.status" color="#3fb950" v-if="item.status === 'Open'"></Badge>
                        <Badge :text="item.status" color="#ab7df8" v-else></Badge>
                    </div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
