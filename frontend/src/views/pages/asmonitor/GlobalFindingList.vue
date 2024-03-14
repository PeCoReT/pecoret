<script>
import ASMonitorService from '@/service/ASMonitorService';
import BlankSlate from '@/components/BlankSlate.vue';
import FindingCreateDialog from '@/components/asmonitor/FindingCreateDialog.vue';
import SeverityBadge from '@/components/SeverityBadge.vue';

export default {
    name: 'GlobalFindingList',
    components: { FindingCreateDialog, BlankSlate, SeverityBadge },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Findings',
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
    methods: {
        getItems() {
            this.loading = true;
            this.service
                .getGlobalFindings(this.$api)
                .then((response) => {
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
                .getGlobalFindings(this.$api, params)
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
                name: 'ASMonitorFindingDetail',
                params: { programId: row.data.program.pk, findingId: row.data.pk }
            });
        },
        confirmDialogDelete(programId, id) {
            this.$confirm.require({
                message: 'Do you want to remove this finding?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteFinding(this.$api, programId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Finding was removed!',
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
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs" />
        </div>
    </div>
    <div class="grid">
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <FindingCreateDialog @object-created="getItems"></FindingCreateDialog>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable @row-click="onRowClick" :paginator="true" dataKey="pk" :rowHover="this.items.length > 0" :rows="pagination.limit" :value="items" :loading="loading" :lazy="true" :totalRecords="totalRecords" @page="onPage">
                    <template #empty>
                        <BlankSlate title="No findings!" text="No targets found!" icon="fa fa-bug"></BlankSlate>
                    </template>
                    <template #header>
                        <div class="grid">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </template>
                    <Column field="name" header="Name"></Column>
                    <Column field="severity" header="Severity">
                        <template #body="slotProps">
                            <SeverityBadge :severity="slotProps.data.severity"></SeverityBadge>
                        </template>
                    </Column>
                    <Column field="target.name" header="Target"></Column>
                    <Column field="status" header="Status"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.program.pk, slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>
