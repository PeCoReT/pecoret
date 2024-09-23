<script>
import ASMonitorService from '@/service/ASMonitorService';
import ProgramCreateDialog from '@/components/dialogs/attack_surface/ProgramCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ProgramUpdateDialog from '@/components/dialogs/attack_surface/ProgramUpdateDialog.vue';
import { useListViewComposable } from '@/composables/listViewComposable';

export default {
    name: 'ProgramList',
    components: { ProgramUpdateDialog, GenericDataTable, BaseListLayout, ProgramCreateDialog },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Programs',
                    disabled: true
                }
            ],
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            filters: {},
            service: new ASMonitorService(),
            listComposable: useListViewComposable()
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.service
                .getPrograms(this.$api, data)
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
            this.getItems({ search: query });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this program?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteProgram(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Program was removed!',
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
        <template #head-right>
            <div class="flex justify-end">
                <ProgramCreateDialog @object-created="getItems"></ProgramCreateDialog>
            </div>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No programs found!"
                blank-slate-title="No Programs!"
                blank-slate-icon="fa fa-shield"
                :model-value="this.items"
                @page="onPage"
                @search="onGlobalSearch"
                :show-search="true"
                @sort="
                    (event) => {
                        listComposable.sort(event, this.getItems);
                    }
                "
                :removable-sort="true"
            >
                <Column field="pk" header="ID"></Column>
                <Column field="name" header="Name" sortable></Column>
                <Column field="date_created" header="Created" sortable></Column>
                <Column field="date_updated" header="Updated" sortable></Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <ProgramUpdateDialog :program="slotProps.data" @object-updated="getItems"></ProgramUpdateDialog>
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
