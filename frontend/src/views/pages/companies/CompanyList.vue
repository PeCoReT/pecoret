<script>
import CompanyService from '@/service/CompanyService';
import CompanyCreateDialog from '../../../components/dialogs/CompanyCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'CompanyList',
    data() {
        return {
            companyService: new CompanyService(),
            breadcrumbs: [{ label: 'Companies', disabled: true }],
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            projectId: this.$route.params.projectId
        };
    },
    mounted() {
        this.getCompanies();
    },
    methods: {
        onGlobalSearch(query) {
            let params = {
                search: query
            };
            this.companyService
                .getCompanies(params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => (this.loading = false));
        },
        getCompanies() {
            this.loading = true;
            let data = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.companyService
                .getCompanies(data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onSort() {},
        onFilter() {},
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getCompanies();
        }
    },
    components: { CompanyCreateDialog, BlankSlate }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <CompanyCreateDialog @object-created="getCompanies"></CompanyCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable
                    :paginator="true"
                    dataKey="pk"
                    :rowHover="items.length > 0"
                    :rows="pagination.limit"
                    :value="items"
                    filterDisplay="menu"
                    :lazy="true"
                    responsiveLayout="scroll"
                    :totalRecords="totalRecords"
                    :loading="loading"
                    @page="onPage"
                    @sort="onSort"
                    @filter="onFilter"
                >
                    <template #header>
                        <div class="flex justify-content-between flex-column sm:flex-row">
                            <span class="p-input-icon-left mb-2">
                                <i class="pi pi-search" />
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </span>
                        </div>
                    </template>

                    <template #empty>
                        <BlankSlate title="No companies!" text="No companies found!" icon="fa fa-globe"></BlankSlate>
                    </template>

                    <Column field="name" header="Name">
                        <template #body="slotProps">
                            <router-link class="text-color underline" :to="{ name: 'CompanyDetail', params: { companyId: slotProps.data.pk } }">
                                {{ slotProps.data.name }}
                            </router-link>
                        </template>
                    </Column>
                    <Column field="street" header="Street"></Column>
                    <Column field="city" header="City"></Column>
                    <Column field="country" header="Country"></Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>