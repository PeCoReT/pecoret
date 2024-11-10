<script>
import TechnologyCreateDialog from '@/components/dialogs/TechnologyCreateDialog.vue';
import TechnologyUpdateDialog from '@/components/dialogs/TechnologyUpdateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import { useListViewComposable } from '@/composables/listViewComposable';

export default {
    name: 'TechnologyList',
    components: { GenericDataTable, BaseListLayout, TechnologyUpdateDialog, TechnologyCreateDialog },
    data() {
        return {
            listComposable: useListViewComposable(),
            loading: false,
            breadcrumbs: [
                {
                    label: 'Technologies',
                    disabled: true
                }
            ],
            items: [],
            totalRecords: 0,
            pagination: { page: 1, limit: 25 },
            filters: {
                source_code_available: { value: null }
            },
            sourceFilterChoices: [
                { value: true, label: 'Yes' },
                { value: false, label: 'No' }
            ]
        };
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getItems(params) {
            this.loading = true;

            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.technologyList, null, data)
                .then((response) => {
                    this.items = response.data.results;
                    this.totalRecords = response.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this technology?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.technologyDetail, {pk: id}).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Technology was removed!',
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
            <TechnologyCreateDialog @object-created="getItems"></TechnologyCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No technologies found!"
                blank-slate-title="No Technologies!"
                blank-slate-icon="fa fa-microship"
                :model-value="items"
                @page="onPage"
                :show-search="true"
                @search="
                    (query) => {
                        this.getItems({ search: query });
                    }
                "
                @filter="getItems"
                v-model:filters="filters"
            >
                <Column field="name" header="Name"></Column>
                <Column field="cpe" header="CPE"></Column>
                <Column field="homepage" header="Homepage"></Column>
                <Column field="source_code_available" :showFilterMatchModes="false" header="Source Code Available">
                    <template #body="slotProps">
                        {{ slotProps.data.source_code_available }}
                    </template>
                    <template #filter="{ filterModel }">
                        <Dropdown v-model="filterModel.value" :show-clear="true" :options="sourceFilterChoices" class="p-column-filter" showClear optionLabel="label" optionValue="value"></Dropdown>
                    </template>
                </Column>
                <Column field="date_updated" header="Updated"></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <TechnologyUpdateDialog :technology="slotProps.data" @object-updated="getItems"></TechnologyUpdateDialog>
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
