<script>
import ProjectService from '@/service/ProjectService';
import { FilterMatchMode } from 'primevue/api';
import { useAuthStore } from '@/store/auth';
import ProjectCreateDialog from '@/components/dialogs/ProjectCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';

const projectService = new ProjectService();
const authStore = useAuthStore();

export default {
    name: 'ProjectList',
    mounted() {
        authStore.deactivateProject();
        this.getProjects();
        this.getPinnedProjects();
    },
    data() {
        return {
            breadcrumbs: [{ label: 'Projects', disabled: true }],
            projects: [],
            pinnedProjects: [],
            loading: false,
            totalRecords: 0,
            selectedProjects: [],
            deleteButtonLoading: false,
            pagination: { page: 1, limit: 20 },
            filters: {
                status: { value: 'Open', matchMode: FilterMatchMode.EQUALS }
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
            this.loading = true;
            let params = {
                search: query
            };
            projectService
                .getProjects(this.$api, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.projects = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
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
                        projectService.deleteProject(this.$api, item.pk).then(() => {
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
            projectService.getProjects(this.$api, params).then((response) => {
                this.pinnedProjects = response.data.results;
            });
        },
        getProjects() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page,
                status: this.filters.status.value
            };
            projectService
                .getProjects(this.$api, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.projects = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onSort(event) {
            this.loading = true;
            let params = {
                ordering: event.sortField
            };
            if (event.sortOrder === -1) {
                params['ordering'] = '-' + event.sortField;
            }
            projectService
                .getProjects(this.$api, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.projects = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onFilter(event) {
            let params = {
                status: event.filters.status.value
            };
            projectService.getProjects(this.$api, params).then((response) => {
                this.totalRecords = response.data.count;
                this.projects = response.data.results;
            });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getProjects();
        },
        onRowClick(row) {
            this.$router.push({
                name: 'ProjectDetail',
                params: {
                    projectId: row.data.pk
                }
            });
        }
    },
    components: { ProjectCreateDialog, BlankSlate }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs" />
        </div>
    </div>

    <div class="grid">
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <ProjectCreateDialog @object-created="getProjects"></ProjectCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid" v-if="pinnedProjects.length > 0">
        <div class="sm:col-6 md:col-4" v-for="project in pinnedProjects" v-bind:key="project.pk">
            <div class="card">
                <router-link class="text-color underline" :to="{ name: 'ProjectDetail', params: { projectId: project.pk } }">
                    {{ project.name }}
                </router-link>
                <br />
                <small>{{ project.status }}</small>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable
                    :paginator="true"
                    dataKey="pk"
                    :rowHover="this.projects.length > 0"
                    :rows="pagination.limit"
                    v-model:selection="selectedProjects"
                    class="p-datatable-gridlines2"
                    :value="projects"
                    filterDisplay="menu"
                    :lazy="true"
                    responsiveLayout="scroll"
                    :totalRecords="totalRecords"
                    :loading="loading"
                    @page="onPage($event)"
                    removableSort
                    filter
                    v-model:filters="filters"
                    @sort="onSort($event)"
                    @filter="onFilter($event)"
                    @row-click="onRowClick"
                >
                    <template #empty>
                        <BlankSlate title="No projects!" text="No projects found!" icon="fa fa-box"></BlankSlate>
                    </template>

                    <template #header>
                        <div class="grid">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                            <Button v-if="selectedProjects.length > 0" icon="fa fa-trash" size="small" outlined severity="danger" @click="bulkDeleteConfirm" class="ml-2"></Button>
                        </div>
                    </template>
                    <Column selectionMode="multiple" headerStyle=""></Column>
                    <Column field="name" header="Name" sortable>
                        <template #body="slotProps">
                            [{{ slotProps.data.year }}] {{ slotProps.data.name }}
                        </template>
                    </Column>
                    <Column field="company_name" header="Company"></Column>
                    <Column field="status" header="Status" :showFilterMatchModes="false">
                        <template #filter="{ filterModel }">
                            <Dropdown v-model="filterModel.value" :options="statusChoices" placeholder="Select One" class="p-column-filter" showClear optionLabel="label" optionValue="value"></Dropdown>
                        </template>
                    </Column>
                    <Column field="date_created" header="Created" sortable></Column>
                    <Column field="test_method" header="Test Method"></Column>
                    <Column field="start_date" header="Start Date"></Column>
                    <Column field="end_date" header="End Date"></Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>
