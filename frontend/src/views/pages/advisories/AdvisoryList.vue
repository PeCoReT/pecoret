<script>
import AdvisoryService from '@/service/AdvisoryService';
import SeverityBadge from '@/components/SeverityBadge.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import { useAuthStore } from '@/store/auth';

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
        onSort() {},
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
            this.service.getAdvisories(this.$api, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page,
                status: this.filters.status.value
            };
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
    components: { SeverityBadge, BlankSlate }
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
            <div class="flex justify-content-end">
                <Button outlined icon="fa fa-plus" label="Advisory" v-if="showCreateButton === true" @click="this.$router.push({ name: 'AdvisoryCreate' })"></Button>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable
                    paginator
                    lazy
                    dataKey="pk"
                    :value="items"
                    :rows="pagination.limit"
                    :totalRecords="totalRecords"
                    filterDisplay="menu"
                    :loading="loading"
                    @sort="onSort"
                    @page="onPage"
                    @filter="onFilter"
                    :rowHover="items.length > 0"
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
                    <Column field="vulnerability_status" header="Vulnerability Status"></Column>
                    <Column field="visibility" header="Visibility"></Column>
                    <Column field="date_planned_disclosure" header="Planned Disclosure"></Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>
