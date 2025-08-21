<script>
import { SeverityDropdownMenu, SortListDropdownMenu } from '@/components/dropdown-menu';
import { DataViewContent, DataViewHeader } from '@/components/dataview';
import { Badge } from '@/components/badge';
import SearchField from '@/partials/common/SearchField.vue';
import { Paginator } from '@/components/paginator';
import { Button } from '@/components/ui/button';
import Select from '@/components/select/Select.vue';
import { commonSortFilter, severityChoices } from '@/utils/constants';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import { listViewMixin } from '@/mixins/listViewMixin';
import { paramMixin } from '@/mixins/params';

export default {
    name: 'FindingList',
    mixins: [listViewMixin, paramMixin],
    components: {
        DataViewListLayout,
        Select,
        Button,
        Paginator,
        SearchField,
        SeverityDropdownMenu,
        Badge,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader
    },
    data() {
        return {
            items: [],
            loading: false,
            filters: {
                ordering: { value: '-date_created' },
                search: { value: null }
            },
            selection: {},
            sortItems: commonSortFilter
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        severityChoices() {
            return severityChoices;
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asFindingList, null, data)
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
        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>
        <template #create-button>
            <Button as-child>
                <a :href="this.$router.resolve({ name: 'AttackSurfaceFindingCreate' }).href"> <i class="fa fa-plus"></i> Finding </a>
            </Button>
        </template>

        <DataViewHeader :show-bulk-select="true" :total-records="totalRecords" v-model:selection="selection" v-model:items="items">
            <template #filters>
                <SortListDropdownMenu :items="sortItems" v-model="filters.ordering.value" @update:model-value="getItems()"></SortListDropdownMenu>
            </template>
            <template #bulk>
                <Select
                    :options="severityChoices()"
                    placeholder="Severity"
                    @update:model-value="
                        (value) => {
                            bulkPatch({ severity: value });
                        }
                    "
                ></Select>
            </template>
        </DataViewHeader>
        <DataViewContent v-model:selection="selection" :items="items" :loading="loading" blank-slate-icon="fa fa-bug" blank-slate-text="No findings here!" blank-slate-title="No Findings!" :show-bulk-select="true">
            <template #item="{ item }">
                <div class="flex-1">
                    <div class="flex justify-between items-center">
                        <div class="font-semibold text-base flex items-center mb-1">
                            <a :href="this.$router.resolve({ name: 'AttackSurfaceFindingDetail', params: { findingId: item.pk } }).href" class="hover:underline">
                                {{ item.title }}
                            </a>
                            <Badge v-if="item.severity" :text="item.severity" :variant="item.severity" class="ml-5"> </Badge>
                        </div>
                    </div>

                    <div class="flex flex-wrap">
                        <span v-for="tag in item.tags" :key="tag.pk" class="bg-background text-accent-foreground text-sm px-2 py-1 rounded border border-gray-800 hover:bg-surface-800 hover:cursor-pointer">
                            {{ tag.name }}
                        </span>
                    </div>

                    <div class="text-xs text-muted-foreground">
                        <span>
                            Created: <span>{{ item.date_created }} by {{ item.created_by_user.username }}</span>
                        </span>
                        <span class="mx-2">|</span>
                        <span>
                            Updated: {{ item.date_updated }}
                            <span v-if="item.updated_by_user">{{ item.updated_by_user.username }}</span>
                        </span>
                    </div>
                </div>
                <div class="flex">
                    <div class="flex items-center space-x-4 text-sm">
                        <span class="font-normal">{{ item.program.name }}</span>
                        <Badge :text="item.status" color="#cbcbcb"></Badge>
                    </div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
