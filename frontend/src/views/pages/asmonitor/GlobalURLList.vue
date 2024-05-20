<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';


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
            items: [],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems(params) {
            this.loading = true;
            if (!params) {
                params = {};
            }
            params['page'] = this.pagination.page;
            params['limit'] = this.pagination.limit;
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
            >
                <Column field="url" header="URL"></Column>
                <Column field="last_seen" header="Last Seen" sortable>
                    <template #body="slotProps">
                        {{ slotProps.data.last_seen || 'Never' }}
                    </template>
                </Column>
                <Column field="program.name" header="Program"></Column>
                <Column field="date_updated" header="Updated" sortable></Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
