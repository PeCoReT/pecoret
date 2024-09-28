<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import URLCreateDialog from '@/components/dialogs/attack_surface/URLCreateDialog.vue';
import TechnologyService from '@/service/TechnologyService';

export default {
    name: 'URLList',
    components: {
        URLCreateDialog,
        GenericDataTable,
        BaseListLayout
    },
    data() {
        return {
            service: new ASMonitorService(),
            items: [],
            loading: false,
            pagination: { limit: 25, page: 1 },
            totalRecords: 0,
            techChoices: [],
            techService: new TechnologyService(),
            selectedItems: [],
            deleteButtonLoading: false,
            filters: {
                technologies: { value: null }
            },
            breadcrumbs: [
                {
                    label: 'URLs',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit,
                technologies: this.filters.technologies.value
            };
            this.service
                .getURLs(params)
                .then((resp) => {
                    this.items = resp.data.results;
                    this.totalRecords = resp.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
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
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onSearch(event) {
            let params = {
                search: event
            };
            this.service.getURLs(params).then((resp) => {
                this.items = resp.data.results;
                this.totalRecords = resp.data.count;
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
                name: 'AttackSurfaceURLDetail',
                params: { urlId: row.data.pk }
            });
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
                        this.service.deleteURL(this.$api, item.pk).then(() => {
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
        }
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <URLCreateDialog @object-created="getItems"></URLCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No urls found!"
                blank-slate-title="No URLs"
                blank-slate-icon="fa fa-sitemap"
                :model-value="items"
                :show-search="true"
                @search="onSearch"
                :show-refresh-button="true"
                @refresh="getItems"
                v-model:filters="filters"
                @filter="getItems"
                @row-click="onRowClick"
                filter-display="menu"
                v-model:selection="selectedItems"
            >
                <template #bulk-edit>
                    <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
                </template>
                <Column selection-mode="multiple" headerStyle=""></Column>
                <Column field="url" header="URL">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.url.length > 120" v-tooltip="slotProps.data.url">{{ slotProps.data.url.substring(0, 120) }}...</span>
                        <span v-else>{{ slotProps.data.url }}</span>
                    </template>
                </Column>
                <Column field="service.target.program.name" header="Program"></Column>
                <Column field="status_code" header="Status Code">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.status_code">{{ slotProps.data.status_code }}</span>
                        <span v-else>-</span>
                    </template>
                </Column>
                <Column header="Technologies" field="technologies" :showFilterMatchModes="false">
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
                <Column field="date_updated" header="Updated"></Column>

            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
