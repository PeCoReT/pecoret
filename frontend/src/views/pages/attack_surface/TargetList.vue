<script>
import ASMonitorService from '@/service/ASMonitorService';
import TargetCreateDialog from '@/components/attack_surface/TargetCreateDialog.vue';
import TargetUpdateDialog from '@/components/attack_surface/TargetUpdateDialog.vue';
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
            selectedItems: [],

            tagChoices: [],
            techChoices: [],
            deleteButtonLoading: false,
            dataTypeChoices: [
                { name: 'Domain', value: 'Domain' },
                { name: 'Subdomain', value: 'Subdomain' },
                { name: 'IP', value: 'IP' },
                { name: 'Network', value: 'Network' }
            ],
            filters: {
                tags: { value: null },
                technologies: { value: null },
                data_type: { value: null },
                scope: { value: null }
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
            if (names.length < 1) {
                return '-';
            }
            return names.join(',');
        },
        bulkDeleteConfirm() {
            this.$confirm.require({
                message: 'Do you want to delete all selected items?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteButtonLoading = true;
                    this.loading = true;
                    let itemsDeleted = 0;
                    this.selectedItems.forEach((item) => {
                        this.service.deleteTarget(this.$api, item.pk).then(() => {
                            itemsDeleted++;
                            if (itemsDeleted === this.selectedItems.length) {
                                this.loading = false;
                                this.deleteButtonLoading = false;
                                this.selectedItems = [];
                                this.getItems();
                            }
                        });
                    });
                }
            });
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
                .getTargets(this.$api, params)
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
                technologies: this.filters.technologies.value,
                data_type: this.filters.data_type.value,
                scope: this.filters.scope.value
            };
            this.service
                .getTargets(this.$api, data)
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
                .getTargets(this.$api, params)
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
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this target?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteTarget(this.$api, id).then(() => {
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
                @page="onPage"
                :removable-sort="true"
                filter-display="menu"
                :show-search="true"
                @search="onGlobalSearch"
                :show-refresh-button="true"
                @refresh="getItems"
                v-model:selection="selectedItems"
            >
                <template #bulk-edit>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
                </template>
                <Column selectionMode="multiple" headerStyle=""></Column>

                <Column field="data" header="Data"></Column>
                <Column field="data_type" header="Data Type" :showFilterMatchModes="false">
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="service.getDataTypeChoices()" :showClear="true" optionLabel="name" optionValue="value"></Dropdown>
                    </template>
                </Column>
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
                <Column field="date_updated" header="Updated" sortable></Column>
                <Column field="scope" header="Scope" :show-filter-match-modes="false">
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :options="service.getInScopeChoices()" optionValue="value" optionLabel="name"></Dropdown>
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <TargetUpdateDialog :target="slotProps.data" @object-updated="getItems"></TargetUpdateDialog>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
