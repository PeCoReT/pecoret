<script>
import AdvisoryService from '@/service/AdvisoryService';
import SeverityBadge from '@/components/SeverityBadge.vue';
import { useAuthStore } from '@/store/auth';
import AdvisoryLabelBadge from '@/components/AdvisoryLabelBadge.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'AdvisoryList',
    data() {
        return {
            service: new AdvisoryService(),
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
                status: { value: 'Not Disclosed' }
            }
        };
    },
    mounted() {
        this.getItems();
    },
    computed: {
        statusChoices() {
            return this.service.getStatusChoices();
        },
        showCreateButton() {
            return this.authStore.groups.isVendor !== true;
        }
    },
    methods: {
        onFilter() {
            this.getItems();
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onGlobalSearch(query) {
            let params = {
                search: query
            };
            this.service.getAdvisories(this.$api, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        onRowClick(row) {
            this.$router.push({
                name: 'AdvisoryDetail',
                params: {
                    advisoryId: row.data.pk
                }
            });
        },
        onSort(event) {
            let params = { ordering: event.sortField };
            if (event.sortOrder === -1) {
                params['ordering'] = '-' + event.sortField;
            }
            this.getItems(params);
        },
        getItems(params) {
            this.loading = true;
            if (!params) {
                params = {};
            }
            params['limit'] = this.pagination.limit;
            params['page'] = this.pagination.page;
            params['status'] = this.filters.status.value;
            this.service
                .getAdvisories(this.$api, params)
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
            <Button outlined icon="fa fa-plus" label="Advisory" v-if="showCreateButton === true" @click="this.$router.push({ name: 'AdvisoryCreate' })"></Button>
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
                @rowClick="onRowClick"
                @filter="onFilter"
                filter-display="menu"
                :filter="true"
                @search="onGlobalSearch"
                :show-search="true"
                :show-refresh-button="true"
                @sort="onSort"
                :removable-sort="true"
                @refresh="getItems"
            >
                <Column field="advisory_id" header="ID" sortable></Column>
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
                        <Dropdown v-model="filterModel.value" :options="statusChoices" placeholder="Select One" class="p-column-filter" showClear optionLabel="label" optionValue="value"></Dropdown>
                    </template>
                </Column>
                <Column field="vulnerability_status" header="Vulnerability Status"></Column>
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
