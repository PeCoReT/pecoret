<script>
import SeverityBadge from '@/components/badges/SeverityBadge.vue';
import { useAuthStore } from '@/store/auth';
import AdvisoryLabelBadge from '@/components/badges/AdvisoryLabelBadge.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import { useListViewComposable } from '@/composables/listViewComposable';
import { advisoryStatusChoices } from '@/utils/constants';

export default {
    name: 'AdvisoryList',
    data() {
        return {
            loading: false,
            authStore: useAuthStore(),
            breadcrumbs: [
                {
                    label: 'Advisories',
                    disabled: true
                }
            ],
            items: [],
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            filters: {
                status: { value: 'Not Disclosed' },
                vulnerability_status: { value: null }
            }
        };
    },
    setup() {
        const { sort, buildParams } = useListViewComposable();
        return { sort, buildParams };
    },
    mounted() {
        this.getItems();
    },
    computed: {
        statusChoices() {
            return advisoryStatusChoices;
        },
        vulnerabilityStatusChoices() {
            return this.vulnerabilityStatusChoices();
        },
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onGlobalSearch(query) {
            this.getItems({ search: query });
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
    components: { GenericDataTable, BaseListLayout, SeverityBadge, AdvisoryLabelBadge }
};
</script>
<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <Button outlined icon="fa fa-plus" label="Advisory" @click="this.$router.push({ name: 'AdvisoryCreate' })"></Button>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No advisories found!"
                blank-slate-title="No Advisories!"
                blank-slate-icon="fa fa-bugs"
                :model-value="items"
                v-model:filters="filters"
                @page="onPage"
                @filter="getItems"
                filter-display="menu"
                :filter="true"
                @search="onGlobalSearch"
                :show-search="true"
                :show-refresh-button="true"
                @sort="sort($event, this.getItems)"
                :removable-sort="true"
                @refresh="getItems"
            >
                <Column field="advisory_id" header="ID" :sortable="true">
                    <template #body="slotProps">
                        <a :href="this.$router.resolve({name: 'AdvisoryDetail', params: {advisoryId: slotProps.data.pk}}).href" class="underline">{{ slotProps.data.advisory_id }}</a>
                    </template>
                </Column>
                <Column field="title" header="Title"></Column>
                <Column field="vulnerability.name" header="Vulnerability"></Column>
                <Column field="severity" header="Severity">
                    <template #body="slotProps">
                        <SeverityBadge :severity="slotProps.data.severity"></SeverityBadge>
                    </template>
                </Column>
                <Column header="Product">
                    <template #body="slotProps">{{ slotProps.data.technology.name }}</template>
                </Column>
                <Column field="status" header="Status" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Select v-model="filterModel.value" :options="statusChoices" placeholder="Select One" class="p-column-filter" showClear optionLabel="label" optionValue="value"></Select>
                    </template>
                </Column>
                <Column field="vulnerability_status" header="Vulnerability Status" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Select v-model="filterModel.value" :options="vulnerabilityStatusChoices" class="p-column-filter" :showClear="true" optionLabel="label" optionValue="value"></Select>
                    </template>
                </Column>
                <Column field="user.username" header="User"></Column>
                <Column field="date_planned_disclosure" header="Planned Disclosure" sortable></Column>
                <Column header="Labels" field="labels" :showFilterMatchModes="false">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.labels && slotProps.data.labels.length < 1">-</span>
                        <AdvisoryLabelBadge v-for="label in slotProps.data.labels" :label="label" :key="label.pk" v-else></AdvisoryLabelBadge>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
