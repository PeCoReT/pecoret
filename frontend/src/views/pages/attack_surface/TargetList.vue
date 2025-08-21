<script>
import { boolYesNo, commonSortFilter, InScopeChoices } from '@/utils/constants';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import { RadioDropdownMenu, SortListDropdownMenu } from '@/components/dropdown-menu';
import { DataViewContent } from '@/components/dataview';
import { Badge } from '@/components/badge';
import ScopeBadge from '@/partials/common/ScopeBadge.vue';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import { ModelCombobox } from '@/components/combobox';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';
import { paramMixin } from '@/mixins/params';

export default {
    name: 'TargetList',
    mixins: [listViewMixin, paramMixin],
    components: {
        Paginator,
        ModelCombobox,
        RadioDropdownMenu,
        DataViewListLayout,
        ScopeBadge,
        Badge,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField
    },
    data() {
        return {
            items: [],
            loading: false,
            selectedItems: [],
            dataTypeChoices: [
                { label: 'Domain', value: 'Domain' },
                { label: 'Subdomain', value: 'Subdomain' },
                { label: 'IP', value: 'IP' }
            ],
            filters: {
                data_type: { value: '' },
                scope: { value: '' },
                search: { value: null },
                ordering: { value: '-date_created' },
                program: { value: this.$route.query.program || '' },
                is_resolved: { value: null }
            },
            scopeDropdownItems: InScopeChoices,
            sortItems: commonSortFilter
        };
    },
    methods: {
        boolYesNo() {
            return boolYesNo;
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.asTargetList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        isNew(dateString) {
            const currentDate = new Date();
            const itemDate = new Date(dateString);
            const timeDifference = currentDate - itemDate;
            const daysDifference = timeDifference / (1000 * 60 * 60 * 24);
            return daysDifference <= 3;
        }
    },
    mounted() {
        this.initFromUrl();
        this.getItems();
    }
};
</script>

<template>
    <DataViewListLayout :search-full-width="true">
        <template #search>
            <SearchField v-model="filters.search.value" @search="getItems()"></SearchField>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <ModelCombobox v-model="this.filters.program.value" :api-endpoint="this.$api.e.asProgramList"
                    label="Program" @select="this.getItems()" :fluid="true"></ModelCombobox>
                <RadioDropdownMenu label="Resolved" :items="boolYesNo()" v-model="filters.is_resolved.value"
                    @select="getItems()"></RadioDropdownMenu>
                <RadioDropdownMenu v-model="filters.data_type.value" :items="dataTypeChoices" label="Data Type"
                    @select="getItems()"></RadioDropdownMenu>
                <RadioDropdownMenu v-model="filters.scope.value" :items="scopeDropdownItems" label="Scope"
                    @select="getItems()"></RadioDropdownMenu>
                <SortListDropdownMenu v-model="filters.ordering.value" :items="sortItems"
                    @update:model-value="getItems()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-crosshairs"
            blank-slate-text="No targets here!" blank-slate-title="No Targets!">
            <template #item="{ item }">
                <div class="flex-1">
                    <div class="flex justify-between items-center">
                        <div class="flex items-center justify-between gap-4">
                            <a :href="this.$router.resolve({ name: 'AttackSurfaceTargetDetail', params: { targetId: item.pk } }).href"
                                class="font-semibold text-base hover:underline">
                                {{ item.data }}
                            </a>
                            <Badge v-if="isNew(item.date_created)" color="#28568d" text="New"></Badge>
                        </div>

                        <div class="flex items-center space-x-4 text-sm">
                            <span class="font-normal">{{ item.program.name }}</span>
                            <ScopeBadge :scope="item.scope"></ScopeBadge>
                        </div>
                    </div>

                    <div class="text-xs text-muted-foreground mt-2">
                        <span>
                            Created: <span class="font-medium">{{ item.date_created }}</span>
                        </span>
                        <span class="mx-2">|</span>
                        <span>
                            Updated: <span class="font-medium">{{ item.date_updated }}</span>
                        </span>
                        <span class="mx-2">|</span>
                        <span> {{ item.data_type }}</span>
                        <span v-if="item.resolved_ip">
                            <span class="mx-2">|</span>
                            <span>{{ item.resolved_ip }}</span>
                        </span>
                    </div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
