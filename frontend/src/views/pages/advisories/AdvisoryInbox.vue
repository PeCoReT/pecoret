<script>
import AdvisoryService from '@/service/AdvisoryService';
import SeverityBadge from '@/components/SeverityBadge.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import AdvisoryLabelBadge from '@/components/AdvisoryLabelBadge.vue';

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
                status: { value: 'Open' },
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
        onRowClick(pk) {
            this.$router.push({ name: 'AdvisoryDetail', params: { advisoryId: pk } });
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
    components: { SeverityBadge, BlankSlate, AdvisoryLabelBadge }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end"></div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <Card>
                <template #content>
                    <DataTable
                        paginator
                        lazy
                        dataKey="pk"
                        :value="items"
                        :rows="pagination.limit"
                        :rowHover="items.length > 0"
                        :totalRecords="totalRecords"
                        filterDisplay="menu"
                        :loading="loading"
                        removableSort
                        @sort="onSort"
                        @page="onPage"
                        @filter="onFilter"
                        v-model:filters="filters"
                    >
                        <template #header>
                            <div class="flex justify-content-between flex-column sm:flex-row">
                                <span class="p-input-icon-left mb-2">
                                    <i class="pi pi-search" />
                                    <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                                </span>
                            </div>
                        </template>
                        <template #empty>
                            <BlankSlate icon="fa fa-bugs" text="No advisories found in inbox!" title="No advisories!"></BlankSlate>
                        </template>

                        <Column field="pk" header="ID">
                            <template #body="slotProps">
                                <router-link class="text-color underline" :to="{ name: 'AdvisoryDetail', params: { advisoryId: slotProps.data.pk } }">
                                    {{ slotProps.data.pk }}
                                </router-link>
                            </template>
                        </Column>
                        <Column field="internal_name" header="Internal Name"></Column>
                        <Column field="vulnerability.name" header="Vulnerability"></Column>
                        <Column field="severity" header="Severity">
                            <template #body="slotProps">
                                <SeverityBadge :severity="slotProps.data.severity"></SeverityBadge>
                            </template>
                        </Column>
                        <Column header="Product">
                            <template #body="slotProps"> {{ slotProps.data.product }} (by {{ slotProps.data.vendor_name }}) </template>
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
                                <AdvisoryLabelBadge v-for="label in slotProps.data.labels" :label="label"></AdvisoryLabelBadge>
                            </template>
                            <template #filter="{ filterModel }">
                                <MultiSelect v-model="filterModel.value" :options="labelChoices" @filter="labelFilter" placeholder="Select labels" filter @focus="labelFilter" class="p-column-filter" showClear optionLabel="name" optionValue="pk">
                                </MultiSelect>
                            </template>
                        </Column>
                    </DataTable>
                </template>
            </Card>
        </div>
    </div>
</template>