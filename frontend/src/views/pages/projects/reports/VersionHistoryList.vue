<script>
import { ReportTabMenu, VersionHistoryCreateDialog } from '@/partials/projects';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'VersionHistoryList',
    mixins: [listViewMixin],
    data() {
        return {
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            items: [],
            loading: false,
            filters: {}
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pReportVersionHistoryList, { pPk: this.projectId, rPk: this.reportId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(versionId) {
            this.$confirm.require({
                message: 'Do you want to delete this change?',
                accept: () => {
                    this.deleteChangeHistoryItem(versionId);
                }
            });
        },
        deleteChangeHistoryItem(versionId) {
            this.$api
                .delete(this.$api.e.pReportVersionHistoryDetail, {
                    pPk: this.projectId,
                    rPk: this.reportId,
                    pk: versionId
                })
                .then(() => {
                    this.$toaster({
                        title: 'Deleted',
                        description: 'Change was deleted!',
                        duration: 3000
                    });
                    this.getItems();
                });
        }
    },
    components: {
        ContainerLayout,
        DataViewContent,
        DataViewHeader,
        ReportTabMenu,
        VersionHistoryCreateDialog
    }
};
</script>

<template>
    <ContainerLayout>
        <template #right-header>
            <VersionHistoryCreateDialog @object-created="getItems"></VersionHistoryCreateDialog>
        </template>
        <template #left-header>
            <ReportTabMenu class="md:max-w-lg"></ReportTabMenu>
        </template>
        <DataViewHeader :total-records="totalRecords">
            <template #filters></template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-clock-rotate-left" blank-slate-text="No version history found!" blank-slate-title="No Version History!">
            <template #item="{ item }">
                <div class="flex-1">
                    {{ item.version }}
                    <div class="flex text-xs text-muted-foreground">
                        {{ item.date }}
                    </div>
                </div>
                <div class="flex-1">
                    {{ item.change }}
                </div>
            </template>
        </DataViewContent>
    </ContainerLayout>
</template>
