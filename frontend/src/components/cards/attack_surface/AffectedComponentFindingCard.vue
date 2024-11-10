<script>
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import { useListViewComposable } from '@/composables/listViewComposable';
import ASFindingComponentCreateDialog from '@/components/dialogs/attack_surface/FindingComponentCreateDialog.vue';
import {findingComponentStatus} from "@/utils/constants";

export default {
    name: 'AffectedComponentFindingCard',
    components: { ASFindingComponentCreateDialog, GenericDataTable },
    data() {
        return {
            findingId: this.$route.params.findingId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 50 },
            listComposable: useListViewComposable(),
            selectedItems: []
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        findingComponentStatus() {
            return findingComponentStatus
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onSearch(query) {
            this.getItems({ search: query });
        },
        getItems(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            data['finding'] = this.findingId;
            this.$api
                .get(this.$api.e.asFindingComponentList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        patchComponent(data) {
            this.$api.patch(this.$api.e.asFindingComponentDetail, { pk: data.pk }, { status: data.status }).then(() => {
                this.$toast.add({
                    severity: 'success',
                    life: 3000,
                    summary: 'Component updated!',
                    detail: 'Component updated successfully!'
                });
            });
        },
        bulkDeleteConfirm() {
            this.$confirm.require({
                message: 'Do you want to delete all selected items?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.loading = true;
                    let itemsDeleted = 0;
                    this.selectedItems.forEach((item) => {
                        this.$api.delete(this.$api.e.asFindingComponentDetail, { pk: item.pk }).then(() => {
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
    <div class="col-span-12 card">
        <div class="flex justify-between items-center py-4">
            <!-- Headline on the left -->
            <h2 class="text-xl font-semibold">Affected Components</h2>

            <ASFindingComponentCreateDialog @object-created="getItems"></ASFindingComponentCreateDialog>
        </div>
        <GenericDataTable
            :total-records="totalRecords"
            :loading="loading"
            :pagination="pagination"
            blank-slate-text="No affected components found!"
            blank-slate-title="No Affected Components!"
            blank-slate-icon="fa fa-plug-circle-exclamation"
            :model-value="items"
            @page="onPage"
            v-model:selection="selectedItems"
            @search="onSearch"
            :show-search="true"
        >
            <template #bulk-edit>
                <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
            </template>
            <Column selectionMode="multiple" headerStyle=""></Column>

            <Column field="component.scheme" header="Affected Service"></Column>
            <Column field="status" header="Status">
                <template #body="slotProps">
                    <Select :options="findingComponentStatus()" optionLabel="name" optionValue="value" v-model="slotProps.data.status" @update:modelValue="patchComponent(slotProps.data)"></Select>
                </template>
            </Column>
        </GenericDataTable>
    </div>
</template>
