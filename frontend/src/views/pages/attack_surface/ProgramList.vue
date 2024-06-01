<script>
import ASMonitorService from '@/service/ASMonitorService';
import ProgramCreateDialog from '@/components/attack_surface/ProgramCreateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'ProgramList',
    components: { GenericDataTable, BaseListLayout, ProgramCreateDialog },
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
            service: new ASMonitorService()
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service
                .getPrograms(this.$api, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onRowClick(row) {
            this.$router.push({
                name: 'ASMonitorProgramDetail',
                params: {
                    programId: row.data.pk
                }
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
                .getPrograms(this.$api, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
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
            <div class="flex justify-content-end">
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
            >
                <Column field="name" header="Name"></Column>
                <Column field="date_created" header="Created"></Column>
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
