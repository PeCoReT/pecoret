<script>
import AdvisoryService from '@/service/AdvisoryService';
import SeverityBadge from '@/components/SeverityBadge.vue';
import AdvisoryLabelBadge from '@/components/AdvisoryLabelBadge.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'AdvisoryInbox',
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
            breadcrumbs: [
                {
                    label: 'Dashboard',
                    to: this.$router.resolve({
                        name: 'AdvisoryManagementDashboard'
                    })
                },
                {
                    label: 'Inbox',
                    disabled: true
                }
            ],
            items: [],
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            filters: {
                status: { value: 'Not Disclosed' },
                labels: { value: null }
            },
            labelChoices: []
        };
    },
    mounted() {
        this.getItems();
    },
    computed: {
        statusChoices() {
            return this.service.getStatusChoices();
        }
    },
    methods: {
        onSort(event) {
            this.loading = true;
            let params = {
                ordering: event.sortField,
                status: this.filters.status.value,
                labels: this.filters.labels.value
            };
            if (event.sortOrder === -1) {
                params['ordering'] = '-' + event.sortField;
            }
            this.service
                .getInbox(this.$api, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
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
            this.service.getInbox(this.$api, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        labelFilter(event) {
            let params = {
                search: event.value
            };
            this.service.getLabels(this.$api, params).then((response) => {
                this.labelChoices = response.data.results;
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
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page,
                status: this.filters.status.value,
                labels: this.filters.labels.value
            };
            this.service
                .getInbox(this.$api, params)
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
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No advisories found!"
                blank-slate-title="No Advisories"
                blank-slate-icon="fa fa-bugs"
                :model-value="items"
                @page="onPage"
                v-model:filters="filters"
                filter-display="menu"
                @rowClick="onRowClick"
                :show-search="true"
                @search="onGlobalSearch"
            >
                <Column field="pk" header="ID"> </Column>
                <Column field="internal_name" header="Internal Name"></Column>
                <Column field="vulnerability.name" header="Vulnerability"></Column>
                <Column field="severity" header="Severity">
                    <template #body="slotProps">
                        <SeverityBadge :severity="slotProps.data.severity"></SeverityBadge>
                    </template>
                </Column>
                <Column header="Product">
                    <template #body="slotProps">{{ slotProps.data.technology.name }} </template>
                </Column>
                <Column field="status" header="Status" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="statusChoices" placeholder="Select One" class="p-column-filter" showClear optionLabel="label" optionValue="value"></Dropdown>
                    </template>
                </Column>
                <Column field="user.username" header="User"></Column>
                <Column field="date_planned_disclosure" header="Planned Disclosure" sortable></Column>
                <Column header="Labels" field="labels" :showFilterMatchModes="false">
                    <template #body="slotProps">
                        <AdvisoryLabelBadge v-for="label in slotProps.data.labels" :label="label" :key="label.pk"></AdvisoryLabelBadge>
                    </template>
                    <template #filter="{ filterModel }">
                        <MultiSelect v-model="filterModel.value" :options="labelChoices" @filter="labelFilter" placeholder="Select labels" filter @focus="labelFilter" class="p-column-filter" showClear optionLabel="name" optionValue="pk">
                        </MultiSelect>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
