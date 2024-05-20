<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';
import TagBadgeButton from '@/components/asmonitor/TagBadgeButton.vue';
import TargetUpdateDialog from '@/components/asmonitor/TargetUpdateDialog.vue';
import TechnologyService from '@/service/TechnologyService';

export default {
    name: 'GlobalTargetList',
    components: { TargetUpdateDialog, TagBadgeButton, GenericDataTable, BaseListLayout },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Hosts',
                    disabled: true
                }
            ],
            service: new ASMonitorService(),
            items: [],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            tagChoices: [],
            techChoices: [],
            techService: new TechnologyService(),
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
        tagFilter(event) {
            let params = {
                search: event.value
            };
            this.service.getTags(this.$api, params).then((response) => {
                this.tagChoices = response.data.results;
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
        getItems(params) {
            this.loading = true;
            if (!params) {
                params = {};
            }
            params['tags'] = this.filters.tags.value;
            params['technologies'] = this.filters.technologies.value;
            params['page'] = this.pagination.page;
            params['limit'] = this.pagination.limit;
            this.service
                .getGlobalTargets(this.$api, params)
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
                name: 'ASMonitorTargetDetail',
                params: {
                    programId: row.data.program.pk,
                    targetId: row.data.pk
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
                blank-slate-text="No targets found!"
                blank-slate-title="No Targets"
                blank-slate-icon="fa fa-crosshairs"
                :model-value="items"
                @page="onPage"
                :show-search="true"
                @search="onSearch"
                @rowClick="onRowClick"
                :removable-sort="true"
                @sort="onSort"
                v-model:filters="filters"
                @filter="getItems"
                filter-display="menu"
            >
                <Column field="name" header="Name"></Column>
                <Column field="ip" header="IP"></Column>
                <Column field="last_seen" header="Last Seen" sortable>
                    <template #body="slotProps">
                        {{ slotProps.data.last_seen || 'Unknown' }}
                    </template>
                </Column>
                <Column field="tags" header="Tags" :showFilterMatchModes="false">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.tags.length > 0"> <TagBadgeButton :label="tag" v-for="tag in slotProps.data.tags" :key="tag.pk"></TagBadgeButton> </span>
                        <span v-else>-</span>
                    </template>
                    <template #filter="{ filterModel }">
                        <MultiSelect v-model="filterModel.value" :options="tagChoices" @filter="tagFilter" placeholder="Select tags" filter @focus="tagFilter" class="p-column-filter" showClear optionLabel="name" optionValue="pk"></MultiSelect>
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
                <Column field="scope" header="Scope"></Column>
                <Column field="date_updated" header="Updated" sortable></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <TargetUpdateDialog :target="slotProps.data" @object-updated="getItems"></TargetUpdateDialog>
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
