<script>
import ASMonitorService from '@/service/ASMonitorService';
import TagCreateDialog from '@/components/asmonitor/TagCreateDialog.vue';
import AdvisoryLabelBadge from '@/components/AdvisoryLabelBadge.vue';
import TagUpdateDialog from '@/components/asmonitor/TagUpdateDialog.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import GenericDataTable from '@/components/elements/table/GenericDataTable.vue';

export default {
    name: 'TagList',
    components: { GenericDataTable, BaseListLayout, TagUpdateDialog, TagCreateDialog, AdvisoryLabelBadge },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Tags',
                    disabled: true
                }
            ],
            pagination: { page: 1, limit: 20 },
            loading: false,
            totalRecords: 0,
            service: new ASMonitorService(),
            items: []
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
                .getTags(this.$api, params)
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
            this.loading = true;
            let params = {
                search: query
            };
            this.service
                .getTags(this.$api, params)
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
                message: 'Do you want to remove this tag?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteTag(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Tag was removed!',
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
            <TagCreateDialog @object-created="this.getItems"></TagCreateDialog>
        </template>
        <template #table>
            <GenericDataTable
                :total-records="totalRecords"
                :loading="loading"
                :pagination="pagination"
                blank-slate-text="No tags found!"
                blank-slate-title="No Tags!"
                blank-slate-icon="fa fa-tags"
                :model-value="items"
                @page="onPage"
                :show-search="true"
                @search="onGlobalSearch"
            >
                <Column field="name" header="Name"></Column>
                <Column field="description" header="Description"></Column>
                <Column header="Preview">
                    <template #body="slotProps">
                        <AdvisoryLabelBadge :label="slotProps.data"></AdvisoryLabelBadge>
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <TagUpdateDialog :tag="slotProps.data" @object-updated="getItems"></TagUpdateDialog>
                        <Button size="small" outlined icon="fa fa-trash" severity="danger" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                    </template>
                </Column>
            </GenericDataTable>
        </template>
    </BaseListLayout>
</template>
