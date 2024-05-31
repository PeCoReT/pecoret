<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';
import URLCreateDialog from '@/components/attack_surface/URLCreateDialog.vue';
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
                .getURLs(this.$api, params)
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
            this.service.getURLs(this.$api, params).then((resp) => {
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
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this url?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteURL(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'URL was removed!',
                            life: 3000
                        });
                        this.getItems();
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
                filter-display="menu"
            >
                <Column field="url" header="URL">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.url.length > 120" v-tooltip="slotProps.data.url">{{ slotProps.data.url.substring(0, 120) }}...</span>
                        <span v-else>{{ slotProps.data.url }}</span>
                    </template>
                </Column>
                <Column field="program.name" header="Program"></Column>
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
                <Column field="last_seen" header="Last Seen">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.last_seen">{{ slotProps.data.last_seen }}</span>
                        <span v-else>Never</span>
                    </template>
                </Column>
                <Column field="date_updated" header="Updated"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
