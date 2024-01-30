<script>
import FindingService from '@/service/FindingService';
import SeverityBadge from '@/components/SeverityBadge.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import FindingCopyDialog from '@/components/dialogs/FindingCopyDialog.vue';
import { FilterMatchMode } from 'primevue/api';
import AssetSelectField from '@/components/elements/forms/AssetSelectField.vue';
import FindingCreateDialog from '@/components/projects/findings/FindingCreateDialog.vue';

export default {
    name: 'FindingList',
    mounted() {
        this.getFindings();
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Findings',
                    disabled: true
                }
            ],
            filters: {
                needs_review: { value: null, matchMode: FilterMatchMode.EQUALS },
                component: { value: null, matchMode: FilterMatchMode.EQUALS }
            },
            filterAsset: null,
            projectId: this.$route.params.projectId,
            findingService: new FindingService(),
            findings: [],
            selectedItems: [],
            deleteButtonLoading: false,
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 }
        };
    },
    methods: {
        getFindings() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.findingService
                .getFindings(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.findings = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onSort() {},
        onFilter(event) {
            this.loading = true;
            let params = {
                needs_review: event.filters.needs_review.value
            };
            if (event.filters.component.value !== null) {
                params[event.filters.component.value.type] = event.filters.component.value.pk;
            }
            this.findingService
                .getFindings(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.findings = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getFindings();
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
                        this.findingService.deleteFinding(this.$api, this.projectId, item.pk).then(() => {
                            itemsDeleted++;
                            if (itemsDeleted === this.selectedItems.length) {
                                this.loading = false;
                                this.deleteButtonLoading = false;
                                this.selectedItems = [];
                                this.getFindings();
                            }
                        });
                    });
                }
            });
        },
        onGlobalSearch(search) {
            this.loading = true;
            let params = {
                search: search
            };
            this.findingService
                .getFindings(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.findings = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { FindingCreateDialog, AssetSelectField, FindingCopyDialog, SeverityBadge, BlankSlate }
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
            <div class="justify-content-start flex"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <FindingCreateDialog :project-id="this.projectId"></FindingCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable
                    :paginator="true"
                    dataKey="pk"
                    :rows="pagination.limit"
                    :value="findings"
                    :rowHover="findings.length > 0"
                    v-model:selection="selectedItems"
                    v-model:filters="filters"
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
                        <div class="grid">
                            <span class="p-input-icon-left mb-2">
                                <i class="pi pi-search" />
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </span>
                            <Button v-if="selectedItems.length > 0" icon="fa fa-trash" outlined severity="danger" @click="bulkDeleteConfirm" class="mb-2 ml-2"></Button>
                        </div>
                    </template>
                    <template #empty>
                        <BlankSlate title="No findings!" text="No findings here!" icon="fa fa-bug"></BlankSlate>
                    </template>
                    <Column selectionMode="multiple" headerStyle=""></Column>

                    <Column field="name" header="Name">
                        <template #body="slotProps">
                            <router-link class="text-color underline" :to="{ name: 'FindingDetail', params: { projectId: this.projectId, findingId: slotProps.data.pk } }">
                                {{ slotProps.data.name }}
                            </router-link>
                        </template>
                    </Column>
                    <Column field="severity" header="Severity">
                        <template #body="slotProps">
                            <SeverityBadge :severity="slotProps.data.severity"></SeverityBadge>
                        </template>
                    </Column>
                    <Column field="component.display_name" filterField="component" header="Asset" :showFilterMatchModes="false">
                        <template #filter="{ filterModel }">
                            <AssetSelectField v-model="filterModel.value"></AssetSelectField>
                        </template>
                    </Column>
                    <Column field="vulnerability.name" header="Vulnerability"></Column>
                    <Column field="unique_id" header="ID"></Column>
                    <Column field="status" header="Status"></Column>
                    <Column field="finding_date" header="Date"></Column>
                    <Column field="needs_review" header="Needs Review" :showFilterMatchModes="false">
                        <template #filter="{ filterModel }">
                            <TriStateCheckbox v-model="filterModel.value"></TriStateCheckbox>
                        </template>
                    </Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <FindingCopyDialog :finding="slotProps.data.pk" @object-created="getFindings"></FindingCopyDialog>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>
