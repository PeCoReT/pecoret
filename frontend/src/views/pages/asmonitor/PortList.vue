<script>
import ASMonitorService from '@/service/ASMonitorService';
import TargetDetailTabMenu from '@/components/asmonitor/TargetDetailTabMenu.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'PortList',
    components: {
        GenericDataTable,
        BaseListLayout,
        TargetDetailTabMenu
    },
    data() {
        return {
            service: new ASMonitorService(),
            programId: this.$route.params.programId,
            targetId: this.$route.params.targetId,
            items: [],
            loading: false,
            pagination: { limit: 25, page: 1 },
            totalRecords: 0,
            breadcrumbs: [
                {
                    label: 'Targets',
                    to: this.$router.resolve({
                        name: 'ASMonitorTargetList',
                        params: {
                            programId: this.$route.params.programId
                        }
                    })
                },
                {
                    label: 'Details',
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
                limit: this.pagination.limit
            };
            this.service
                .getPorts(this.$api, this.programId, this.targetId, params)
                .then((resp) => {
                    this.items = resp.data.results;
                    this.totalRecords = resp.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onSearch(event) {
            let params = {
                search: event
            };
            this.service.getPorts(this.$api, this.programId, this.targetId, params).then((resp) => {
                this.items = resp.data.results;
                this.totalRecords = resp.data.count;
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this port?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deletePort(this.$api, this.programId, this.targetId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Port was removed!',
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
    }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #default>
            <TargetDetailTabMenu class="surface-card"></TargetDetailTabMenu>
            <div class="card border-noround-top">
                <GenericDataTable
                    :total-records="totalRecords"
                    :loading="loading"
                    :pagination="pagination"
                    blank-slate-text="No ports found!"
                    blank-slate-title="No Ports"
                    blank-slate-icon="fa fa-network-wired"
                    :model-value="items"
                    :show-search="true"
                    @search="onSearch"
                >
                    <Column field="port" header="Port"></Column>
                    <Column field="service" header="Service"></Column>
                    <Column field="protocol" header="Protocol"></Column>
                    <Column field="banner" header="Banner"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </GenericDataTable>
            </div>
        </template>
    </BaseListLayout>
</template>
