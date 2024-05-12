<script>
import ASMonitorService from '@/service/ASMonitorService';
import TargetDetailTabMenu from '@/components/asmonitor/TargetDetailTabMenu.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'HostnamesList',
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
                    label: 'Hosts',
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
                .getHostnames(this.$api, this.programId, this.targetId, params)
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
            this.service.getHostnames(this.$api, this.programId, this.targetId, params).then((resp) => {
                this.items = resp.data.results;
                this.totalRecords = resp.data.count;
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this hostname?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteHostname(this.$api, this.programId, this.targetId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Hostname was removed!',
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
                    blank-slate-text="No hostnames found!"
                    blank-slate-title="No hostnames"
                    blank-slate-icon="fa fa-name"
                    :model-value="items"
                    :show-search="true"
                    @search="onSearch"
                >
                    <Column field="name" header="Name"></Column>
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
