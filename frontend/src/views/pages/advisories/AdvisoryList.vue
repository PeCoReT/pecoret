<script>
import { useAuthStore } from '@/store/auth';
import { advisoryStatusChoices, severityChoices, vulnerabilityStatusChoices } from '@/utils/constants';
import { Badge } from '@/components/badge';
import { Button } from '@/components/ui/button';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Paginator } from '@/components/paginator';
import RadioDropdownMenu from '@/components/dropdown-menu/RadioDropdownMenu.vue';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { listViewMixin } from '@/mixins/listViewMixin';
import { paramMixin } from '@/mixins/params';

export default {
    name: 'AdvisoryList',
    mixins: [listViewMixin, paramMixin],
    data() {
        return {
            loading: false,
            authStore: useAuthStore(),
            items: [],
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            sortItems: [
                {
                    label: 'Date Created',
                    value: 'date_created'
                },
                {
                    label: 'Date Updated',
                    value: 'date_updated'
                },
                {
                    label: 'Planned Disclosure',
                    value: 'date_planned_disclosure'
                },
                {
                    label: 'ID',
                    value: 'advisory_id'
                }
            ],
            statusChoices: advisoryStatusChoices,
            vulnerabilityStatusChoices: vulnerabilityStatusChoices,
            severityChoices: severityChoices,
            filters: {
                status: { value: 'Not Disclosed' },
                vulnerability_status: { value: null },
                labels: { value: null },
                severity: { value: null },
                technology: { value: null },
                ordering: { value: '-date_created' },
                search: { value: null }
            }
        };
    },
    mounted() {
        this.initFromUrl();
        this.getItems();
    },
    methods: {
        filter(key, value) {
            this.filters[key].value = value;
            this.getItems();
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.advisoryList, null, data)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {
        ModelCombobox,
        RadioDropdownMenu,
        Paginator,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        DataViewListLayout,
        Badge,
        Button
    }
};
</script>
<template>
    <DataViewListLayout>
        <template #search>
            <SearchField v-model="filters.search.value" @search="getItems()"></SearchField>
        </template>
        <template #create-button>
            <Button @click="this.$router.push({ name: 'AdvisoryCreate' })"
                ><i class="fa fa-plus" />
                Advisory
            </Button>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <ModelCombobox :fluid="true" v-model="filters.labels.value" :api-endpoint="this.$api.e.aLabelList" @select="getItems()" label="Label"></ModelCombobox>
                <ModelCombobox :fluid="true" v-model="filters.technology.value" :api-endpoint="this.$api.e.technologyList" @select="getItems()" label="Product"></ModelCombobox>
                <RadioDropdownMenu label="Vulnerability Status" :items="vulnerabilityStatusChoices" v-model="filters.vulnerability_status.value" @select="getItems()"></RadioDropdownMenu>
                <RadioDropdownMenu label="Status" :items="statusChoices" v-model="filters.status.value" @select="getItems()"></RadioDropdownMenu>
                <RadioDropdownMenu label="Severity" :items="severityChoices" v-model="filters.severity.value" @select="getItems()"></RadioDropdownMenu>
                <SortListDropdownMenu :items="sortItems" v-model="filters.ordering.value" @update:model-value="this.getItems()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-title="No Advisories!" blank-slate-text="No advisories found!" blank-slate-icon="fa fa-bugs">
            <template #item="{ item }">
                <div class="flex-1">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-base flex items-center">
                                <a :href="this.$router.resolve({ name: 'AdvisoryDetail', params: { advisoryId: item.pk } }).href" class="hover:underline">{{ item.advisory_id }} / {{ item.title }}</a>
                                <Badge :text="item.severity" :variant="item.severity" class="ml-2"></Badge>
                            </p>
                        </div>
                        <Badge class="ml-5" v-if="item.vulnerability_status === 'Fixed'" variant="closed" :text="item.vulnerability_status"></Badge>
                        <Badge class="ml-5" v-else variant="open" :text="item.vulnerability_status"></Badge>
                    </div>
                    <div class="flex items-center mt-2">
                        <div class="flex-1 text-xs text-muted-foreground">
                            <p class="inline-block"><strong>Status:</strong> {{ item.status }}</p>
                            <p class="inline-block ml-5"><strong>User:</strong> {{ item.user.username }}</p>
                            <p class="inline-block ml-5"><strong>Planned Disclosure Date:</strong> {{ item.date_planned_disclosure }}</p>
                        </div>
                        <div v-for="label in item.labels" class="flex flex-wrap ml-2">
                            <Badge :color="label.color" :text="label.name"></Badge>
                        </div>
                    </div>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
