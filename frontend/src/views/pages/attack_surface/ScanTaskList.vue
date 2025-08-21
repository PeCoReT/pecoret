<script>
import { listViewMixin } from '@/mixins/listViewMixin';
import { asScanTaskStatus, commonSortFilter } from '@/utils/constants';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import ScanStatusBadge from '@/partials/attack_surface/ScanStatusBadge.vue';
import { Paginator } from '@/components/paginator';
import PageHeader from '@/components/typography/PageHeader.vue';
import BackLinkButton from '@/components/button/BackLinkButton.vue';
import RadioDropdownMenu from '@/components/dropdown-menu/RadioDropdownMenu.vue';
import { paramMixin } from '@/mixins/params';

export default {
    name: 'ScanTaskList',
    components: {
        RadioDropdownMenu,
        BackLinkButton,
        PageHeader,
        Paginator,
        ScanStatusBadge,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        DataViewListLayout
    },
    mixins: [listViewMixin, paramMixin],
    data() {
        return {
            items: [],
            loading: false,
            filters: {
                search: { value: null },
                ordering: { value: '-date_updated' },
                status: { value: null }
            },
            statusChoices: asScanTaskStatus,
            sortItems: commonSortFilter
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
                .get(this.$api.e.asScanTaskList, {}, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
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
            <PageHeader>Scan Tasks</PageHeader>
        </template>
        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <RadioDropdownMenu label="Status" :items="statusChoices" v-model="filters.status.value" @select="getItems()"></RadioDropdownMenu>
                <SortListDropdownMenu :items="sortItems" v-model="filters.ordering.value" @update:model-value="this.getItems()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent v-model:items="items" :loading="loading" blank-slate-icon="fa fa-tasks" blank-slate-text="No scan tasks found!" blank-slate-title="No Scan Tasks!">
            <template #item="{ item }">
                <div class="flex-1">
                    <a :href="this.$router.resolve({ name: 'AttackSurfaceScanTaskDetail', params: { taskId: item.pk } }).href" class="hover:underline"> [{{ item.scan_template.scan_type }}] {{ item.pk }} ({{ item.scan_template.name }}) </a>
                    <div class="flex text-xs text-muted-foreground">
                        <span>
                            Created: <span>{{ item.date_created }}</span>
                        </span>
                        <span class="mx-2">|</span>
                        <span> Updated: {{ item.date_updated }} </span>
                    </div>
                </div>
                <div>
                    <ScanStatusBadge :status="item.status"></ScanStatusBadge>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
