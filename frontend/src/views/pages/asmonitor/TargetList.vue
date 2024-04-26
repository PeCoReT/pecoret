<script>
import ASMonitorService from '@/service/ASMonitorService';
import TargetCreateDialog from '@/components/asmonitor/TargetCreateDialog.vue';
import TargetUpdateDialog from '@/components/asmonitor/TargetUpdateDialog.vue';
import TagBadgeButton from '@/components/asmonitor/TagBadgeButton.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';
import TechnologyService from '@/service/TechnologyService';

export default {
    name: 'TargetList',
    components: {
        GenericDataTable,
        BaseListLayout,
        TargetUpdateDialog,
        TargetCreateDialog,
        TagBadgeButton
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Targets',
                    disabled: true
                }
            ],
            service: new ASMonitorService(),
            techService: new TechnologyService(),
            items: [],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            tagChoices: [],
            techChoices: [],
            programId: this.$route.params.programId,
            filters: {
                tags: { value: null },
                technologies: { value: null }
            }
        };
    },
    methods: {
        getTechnologyDisplay(item) {
            let names = [];
            if (item.technologies && item.technologies.length > 0) {
                item.technologies.forEach((item) => {
                    names.push(item.name);
                });
            }
            return names.join(',');
        },
        onSort(event) {
            this.loading = true;
            let params = {
                ordering: event.sortField,
                tags: this.filters.tags.value
            };
            if (event.sortOrder === -1) {
                params['ordering'] = `-${event.sortField}`;
            }
            this.service
                .getTargets(this.$api, this.programId, params)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getItems() {
            this.loading = true;
            let data = {
                limit: this.pagination.limit,
                page: this.pagination.page,
                tags: this.filters.tags.value,
                technologies: this.filters.technologies.value
            };
            this.service
                .getTargets(this.$api, this.programId, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onGlobalSearch(query) {
            this.loading = true;
            let params = {
                search: query
            };
            this.service
                .getTargets(this.$api, this.programId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
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
        onRowClick(row) {
            this.$router.push({
                name: 'ASMonitorTargetDetail',
                params: {
                    programId: this.programId,
                    targetId: row.data.pk
                }
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this target?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteTarget(this.$api, this.programId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Target was removed!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    },
    mounted() {
        this.getItems();
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <TargetCreateDialog @object-created="getItems"></TargetCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No targets found!"
                blank-slate-title="No Targets!"
                blank-slate-icon="fa fa-crosshairs"
                :model-value="items"
                @sort="onSort"
                @filter="getItems"
                v-model:filters="filters"
                :removable-sort="true"
                filter-display="menu"
                :show-search="true"
                @search="onGlobalSearch"
                @row-click="onRowClick"
            >
                <Column field="name" header="Name" sortable></Column>
                <Column field="ip" header="IP"></Column>
                <Column field="last_seen" header="Last Seen" sortable>
                    <template #body="slotProps">
                        {{ slotProps.data.last_seen || 'Unknown' }}
                    </template>
                </Column>
                <Column field="tags" header="Tags" :showFilterMatchModes="false">
                    <template #body="slotProps">
                        <TagBadgeButton :label="tag" v-for="tag in slotProps.data.tags" :key="tag.pk"></TagBadgeButton>
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
