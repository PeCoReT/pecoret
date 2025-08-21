<script>
import { Badge } from '@/components/badge';
import { FindingBulkEditDialog, FindingCopyDialog } from '@/partials/projects';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter, findingStatusChoices, severityChoices } from '@/utils/constants';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Button } from '@/components/ui/button';
import RadioDropdownMenu from '@/components/dropdown-menu/RadioDropdownMenu.vue';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'FindingList',
    mixins: [listViewMixin],
    mounted() {
        this.getItems();
    },
    data() {
        return {
            filters: {
                search: { value: null },
                needs_review: { value: null },
                asset: { value: null },
                severity: { value: null },
                status: { value: null }
            },
            projectId: this.$route.params.projectId,
            findings: [],
            selectedItems: [],
            deleteButtonLoading: false,
            loading: false,
            needsReviewChoices: [
                { label: 'Yes', value: 'true' },
                { label: 'No', value: 'false' }
            ],
            statusFilterChoices: findingStatusChoices
        };
    },
    methods: {
        severityChoices() {
            return severityChoices;
        },
        commonSortFilter() {
            return commonSortFilter;
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pFindingList, { pPk: this.projectId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.findings = response.data.results;
                    this.selectedItems = [];
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {
        Paginator,
        ModelCombobox,
        RadioDropdownMenu,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        DataViewListLayout,
        FindingBulkEditDialog,
        FindingCopyDialog,
        Badge,
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
            <Button :href="this.$router.resolve({ name: 'FindingCreate', params: { projectId: this.projectId } }).href" as="a"><i class="fa fa-plus"></i> Finding </Button>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <ModelCombobox v-model="filters.asset.value" :api-endpoint="this.$api.e.pAssetList" :url-args="{ pPk: this.projectId }" :fluid="true" label="Asset" @select="getItems()"> </ModelCombobox>
                <RadioDropdownMenu label="Needs Review" :items="needsReviewChoices" v-model="filters.needs_review.value" @select="getItems()"></RadioDropdownMenu>
                <RadioDropdownMenu label="Severity" :items="severityChoices()" v-model="filters.severity.value" @select="getItems()"></RadioDropdownMenu>
                <RadioDropdownMenu label="Status" :items="statusFilterChoices" v-model="filters.status.value" @select="getItems()"></RadioDropdownMenu>
                <SortListDropdownMenu :items="commonSortFilter()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent :items="findings" :loading="loading" blank-slate-icon="fa fa-bugs" blank-slate-text="No findings here!" blank-slate-title="No Findings!">
            <template #item="{ item }">
                <strong>{{ item.unique_id }}</strong>
                <div class="flex-1">
                    <div class="flex justify-between items-center">
                        <div class="font-semibold text-base flex items-center mb-1">
                            <a :href="this.$router.resolve({ name: 'FindingDetail', params: { projectId: this.projectId, findingId: item.pk } }).href" class="hover:underline">
                                {{ item.name }}
                            </a>
                            <Badge :text="item.severity" :variant="item.severity" class="ml-5"></Badge>
                        </div>
                    </div>
                    <div class="flex text-xs text-muted-foreground">
                        {{ item.vulnerability.name }}
                    </div>
                    <div class="flex text-xs text-muted-foreground">
                        <span>Created: {{ item.date_created }}</span>
                        <span class="mx-2">|</span>
                        <span>Updated: {{ item.date_updated }}</span>
                    </div>
                </div>
                <div class="flex">
                    <Badge :text="item.status" :variant="item.status"></Badge>
                </div>
                <div class="flex flex-wrap">
                    <span class="text-sm text-muted-foreground">{{ item.asset.name }}</span>
                </div>
                <FindingCopyDialog :finding="item.pk" @object-created="getItems"></FindingCopyDialog>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
