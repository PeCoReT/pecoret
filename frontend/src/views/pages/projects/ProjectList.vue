<script>
import { useAuthStore } from '@/store/auth';
import ProjectCreateDialog from '@/components/dialogs/ProjectCreateDialog.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import { useListViewComposable } from '@/composables/listViewComposable';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';

export default {
    name: 'ProjectList',
    mounted() {
        this.authStore.deactivateProject();
        this.getProjects();
        this.getPinnedProjects();
    },
    data() {
        return {
            breadcrumbs: [{ label: 'Projects', disabled: true }],
            authStore: useAuthStore(),
            listComposable: useListViewComposable(),
            projects: [],
            pinnedProjects: [],
            loading: false,
            totalRecords: 0,
            selectedProjects: [],
            deleteButtonLoading: false,
            pagination: { page: 1, limit: 20 },
            filters: {
                status: { value: 'Open' }
            },
            statusChoices: [
                {
                    label: 'Open',
                    value: 'Open'
                },
                {
                    label: 'Closed',
                    value: 'Closed'
                }
            ]
        };
    },
    methods: {
        onGlobalSearch(query) {
            this.getProjects({ search: query });
        },
        bulkDeleteConfirm() {
            this.$confirm.require({
                message: 'Do you want all selected projects?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteButtonLoading = true;
                    this.loading = true;
                    let itemsDeleted = 0;
                    this.selectedProjects.forEach((item) => {
                        this.$api.delete(this.$api.e.projectDetail, { pk: item.pk }).then(() => {
                            itemsDeleted++;
                            if (itemsDeleted === this.selectedProjects.length) {
                                this.loading = false;
                                this.deleteButtonLoading = false;
                                this.selectedProjects = [];
                                this.getProjects();
                            }
                        });
                    });
                }
            });
        },
        getPinnedProjects() {
            let params = {
                pinned: true
            };
            this.$api.get(this.$api.e.projectList, null, params).then((response) => {
                this.pinnedProjects = response.data.results;
            });
        },
        getProjects(params) {
            this.loading = true;
            let data = this.listComposable.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.projectList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.projects = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getProjects();
        },
        getProjectLink(pk){
            return this.$router.resolve({
                name: 'ProjectDetail',
                params: {
                    projectId: pk
                }
            }).href
        }
    },
    components: { BaseListLayout, GenericDataTable, ProjectCreateDialog }
};
</script>

<template>
    <BaseListLayout :breadcrumbs="breadcrumbs">
        <template #create-button>
            <ProjectCreateDialog @object-created="getProjects"></ProjectCreateDialog>
        </template>
        <template #default>
            <div class="mb-3 mt-3 grid sm:grid-cols-2 md:grid-cols-6 gap-4" v-if="pinnedProjects.length > 0">
                <div class="" v-for="project in pinnedProjects" v-bind:key="project.pk">
                    <div class="card">
                        <router-link class="text-color underline" :to="{ name: 'ProjectDetail', params: { projectId: project.pk } }">
                            {{ project.name }}
                        </router-link>
                        <br />
                        <small>{{ project.status }} / {{ project.company.name }}</small>
                    </div>
                </div>
            </div>

            <div class="card">
                <GenericDataTable
                    :total-records="totalRecords"
                    :loading="loading"
                    :pagination="pagination"
                    blank-slate-text="No projects found!"
                    blank-slate-title="No Projects!"
                    blank-slate-icon="fa fa-box"
                    :model-value="projects"
                    :removable-sort="true"
                    @sort="
                        (event) => {
                            this.listComposable.sort(event, this.getProjects);
                        }
                    "
                    @filter="getProjects"
                    :show-search="true"
                    filter-display="menu"
                    v-model:filters="filters"
                    v-model:selection="selectedProjects"
                    :show-refresh-button="true"
                    @refresh="getProjects"
                    @search="onGlobalSearch"
                >
                    <template #bulk-edit>
                        <Button v-if="selectedProjects.length > 0" icon="fa fa-trash" size="small" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
                    </template>
                    <Column selectionMode="multiple" headerStyle=""></Column>
                    <Column field="name" header="Name" :sortable="true">
                        <template #body="slotProps">
                            <a :href="getProjectLink(slotProps.data.pk)" class="underline">[{{ slotProps.data.year }}] {{ slotProps.data.name }}</a></template>
                    </Column>
                    <Column field="company.name" header="Company">
                        <template #body="slotProps">
                            <a :href="this.$router.resolve({name: 'CompanyDetail', params: {companyId: slotProps.data.company.pk}}).href" class="underline">{{ slotProps.data.company.name }}</a>
                        </template>
                    </Column>
                    <Column field="status" header="Status" :showFilterMatchModes="false">
                        <template #filter="{ filterModel }">
                            <Select v-model="filterModel.value" :options="statusChoices" placeholder="Select One" class="p-column-filter" showClear optionLabel="label" optionValue="value"></Select>
                        </template>
                    </Column>
                    <Column field="date_created" header="Created" :sortable="true"></Column>
                    <Column field="test_method" header="Test Method"></Column>
                    <Column field="visibility" header="Visibility"></Column>
                    <Column field="start_date" header="Period">
                        <template #body="slotProps"> {{ slotProps.data.start_date }} - {{ slotProps.data.end_date }} </template>
                    </Column>
                </GenericDataTable>
            </div>
        </template>
    </BaseListLayout>
</template>
