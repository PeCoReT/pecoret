<script>
import ReportService from '@/service/ReportService';
import ReportCreateDialog from '@/components/dialogs/ReportCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'ReportList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Reports',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            reportService: new ReportService()
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        onSort() {},
        onFilter() {},
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.reportService
                .getReports(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onGlobalSearch(query) {
            let params = {
                search: query
            };
            this.reportService
                .getReports(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { ReportCreateDialog, BlankSlate }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <ReportCreateDialog @object-created="getItems"></ReportCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable paginator lazy dataKey="pk" :rowHover="items.length > 0" :value="items" :rows="pagination.limit" :totalRecords="totalRecords" filterDisplay="menu" :loading="loading" @page="onPage" @sort="onSort" @filter="onFilter">
                    <template #header>
                        <div class="flex justify-content-between flex-column sm:flex-row">
                            <span class="p-input-icon-left mb-2">
                                <i class="pi pi-search" />
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </span>
                        </div>
                    </template>
                    <template #empty>
                        <BlankSlate icon="fa fa-file" text="No reports!" title="No reports found!"></BlankSlate>
                    </template>
                    <Column field="name" header="Name">
                        <template #body="slotProps">
                            <router-link class="text-color underline" :to="{ name: 'ReportDetail', params: { projectId: this.projectId, reportId: slotProps.data.pk } }">
                                {{ slotProps.data.name }}
                            </router-link>
                        </template>
                    </Column>
                    <Column field="variant" header="Variant"></Column>
                    <Column field="template.name" header="Template"></Column>
                    <Column field="author.username" header="Author"></Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>