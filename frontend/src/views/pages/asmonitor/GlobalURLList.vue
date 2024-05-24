<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';
import TechnologyService from '@/service/TechnologyService';

export default {
    name: 'GlobalURLList',
    components: { GenericDataTable, BaseListLayout },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'URLs',
                    disabled: true
                }
            ],
            service: new ASMonitorService(),
            techService: new TechnologyService(),
            techChoices: [],
            items: [],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            filters: {
                tags: { value: null },
                technologies: { value: null }
            }
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getTechnologyDisplay(item) {
            let names = [];
            if (item.technologies && item.technologies.length > 0) {
                item.technologies.forEach((item) => {
                    names.push(item.name);
                });
            }
            if (names.length < 1) {
                return '-';
            }
            return names.join(',');
        },
        getItems(params) {
            this.loading = true;
            if (!params) {
                params = {};
            }
            params['page'] = this.pagination.page;
            params['limit'] = this.pagination.limit;
            params['tags'] = this.filters.tags.value;
            params['technologies'] = this.filters.technologies.value;
            this.service
                .getGlobalURLs(this.$api, params)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onRowClick(row) {
            this.$router.push({
                name: 'ASMonitorURLList',
                params: {
                    programId: row.data.program.pk,
                    targetId: row.data.target.pk
                }
            });
        },
        techFilter(event) {
            let params = {
                search: event.value
            };
            this.techService.getTechnologies(this.$api, params).then((response) => {
                this.techChoices = response.data.results;
            });
        },
        onSearch(query) {
            let params = {
                search: query
            };
            this.getItems(params);
        },
        onSort(event) {
            let params = {
                ordering: event.sortField
            };
            if (event.sortOrder === -1) {
                params['ordering'] = `-${event.sortField}`;
            }
            this.getItems(params);
        }
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No urls found!"
                blank-slate-title="No URLs"
                blank-slate-icon="fa fa-sitemap"
                :model-value="items"
                @page="onPage"
                :show-search="true"
                @search="onSearch"
                @rowClick="onRowClick"
                :removable-sort="true"
                @sort="onSort"
                v-model:filters="filters"
                @filter="getItems()"
                filter-display="menu"
            >
                <Column field="url" header="URL"></Column>
                <Column field="last_seen" header="Last Seen" sortable>
                    <template #body="slotProps">
                        {{ slotProps.data.last_seen || 'Never' }}
                    </template>
                </Column>
                <Column field="technologies" header="Technologies" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <MultiSelect
                            v-model="filterModel.value"
                            :options="techChoices"
                            @filter="techFilter"
                            placeholder="Select technologies"
                            filter
                            @focus="techFilter"
                            class="p-column-filter"
                            showClear
                            optionLabel="name"
                            optionValue="pk"
                        ></MultiSelect>
                    </template>
                    <template #body="slotProps">
                        {{ getTechnologyDisplay(slotProps.data) }}
                    </template>
                </Column>
                <Column field="program.name" header="Program"></Column>
                <Column field="date_updated" header="Updated" sortable></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
