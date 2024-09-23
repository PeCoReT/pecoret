<script>
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ASMonitorService from '@/service/ASMonitorService';
import { useListViewComposable } from '@/composables/listViewComposable';
import TargetPortCreateDialog from '@/components/dialogs/attack_surface/TargetPortCreateDialog.vue';
import PortUpdateDialog from '@/components/dialogs/attack_surface/PortUpdateDialog.vue';

export default {
    name: 'HostPortTable',
    components: { PortUpdateDialog, TargetPortCreateDialog, GenericDataTable },
    props: {
        host: {
            required: true
        }
    },
    data() {
        return {
            loading: false,
            loaded: false,
            totalRecords: 0,
            items: [],
            selectedItems: [],
            service: new ASMonitorService(),
            pagination: { limit: 200, page: 1 },
            listComposable: useListViewComposable()
        };
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onSearch(event) {
            this.getItems({ search: event });
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
                        this.service.deletePort(item.pk).then(() => {
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
        getItems(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, {}, params);
            data['host'] = this.host.pk;
            this.service
                .getPorts(this.$api, data)
                .then((resp) => {
                    this.items = resp.data.results;
                    this.totalRecords = resp.data.count;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    watch: {
        host: {
            deep: true,
            immediate: true,
            handler(value) {
                if (value && value.pk && this.loaded === false) {
                    this.getItems();
                    this.loaded = true;
                }
            }
        }
    }
};
</script>

<template>
    <GenericDataTable
        :total-records="totalRecords"
        :loading="loading"
        :pagination="pagination"
        blank-slate-text="No ports found!"
        blank-slate-title="No Ports!"
        blank-slate-icon="fa fa-circle-nodes"
        v-model="items"
        :show-search="true"
        @page="onPage"
        @search="onSearch"
        v-model:selection="selectedItems"
    >
        <template #bulk-edit>
            <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
        </template>
        <Column selectionMode="multiple" headerStyle=""></Column>
        <Column field="number" header="Port Number"></Column>
        <Column field="protocol" header="Protocol"></Column>
        <Column field="service_name" header="Service"></Column>
        <Column field="technologies" header="Technologies" :showFilterMatchModes="false">
            <template #body="slotProps">
                {{ getTechnologyDisplay(slotProps.data) }}
            </template>
        </Column>
        <Column field="date_updated" header="Date Updated"></Column>
        <Column header="Actions">
            <template #body="slotProps">
                <PortUpdateDialog :port="slotProps.data" @object-updated="getItems"></PortUpdateDialog>
            </template>
        </Column>
        <template #header-right>
            <TargetPortCreateDialog :target="host" @object-created="getItems"></TargetPortCreateDialog>
        </template>
    </GenericDataTable>
</template>
