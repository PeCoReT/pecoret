<script>
import ProjectService from '@/service/ProjectService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import ProjectUpdateDialog from '@/components/dialogs/ProjectUpdateDialog.vue';
import markdown from '@/utils/markdown';
import DashboardSeverityChart from '@/components/pages/projects/DashboardSeverityChart.vue';
import DashboardFindingsCount from '@/components/pages/projects/DashboardFindingsCount.vue';
import LatestFindingsDashboard from '@/components/projects/LatestFindingsDashboard.vue';

const projectService = new ProjectService();

export default {
    name: 'ProjectDetail',
    data() {
        return {
            projectId: this.$route.params.projectId,
            project: {},
            role: {},
            breadcrumbs: [
                { label: 'Projects', to: this.$router.resolve({ name: 'ProjectList' }) },
                { label: 'Project Detail', disabled: true }
            ],
            statusChoices: [
                { label: 'Open', value: 'Open' },
                { label: 'Closed', value: 'Closed' }
            ]
        };
    },
    mounted() {
        this.getProject();
        this.getMembership();
    },
    methods: {
        getProject() {
            projectService.getProject(this.projectId).then((response) => {
                this.project = response.data;
                this.breadcrumbs[this.breadcrumbs.length - 1] = {
                    label: response.data.name,
                    disabled: true
                };
            });
        },
        renderMarkdown(text) {
            if (!text) {
                return '';
            }
            return markdown.renderMarkdown(text);
        },
        getMembership() {
            projectService.getProjectMembershipMe(this.projectId).then((response) => {
                this.role = response.data;
            });
        },
        getPentestTypeDisplay() {
            if (!this.project.pentest_types) {
                return '';
            }
            let pentestTypeNames = [];
            this.project.pentest_types.forEach((element) => {
                pentestTypeNames.push(element.name);
            });
            return pentestTypeNames.join(', ');
        },
        patchProject(data) {
            projectService.patchProject(this.$api, this.projectId, data).then((response) => {
                this.project = response.data;
            });
        },
        pinProject() {
            projectService.pinProject(this.$api, this.projectId, this.project.pinned).then(() => {});
        }
    },
    computed: {
        projectDateDisplay() {
            return this.project.start_date + ' - ' + this.project.end_date;
        }
    },
    components: {
        LatestFindingsDashboard,
        DashboardFindingsCount,
        DetailCardWithIcon,
        ProjectUpdateDialog,
        InfoCardWithForm,
        DashboardSeverityChart
    }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="flex justify-content-end">
                <ProjectUpdateDialog :project="project" @object-updated="getProject"></ProjectUpdateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12 md:col-6 lg:col-6 xl:col-3">
            <DetailCardWithIcon title="Dates" :text="projectDateDisplay" icon="fa-calendar"></DetailCardWithIcon>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-3">
            <DetailCardWithIcon title="Role" icon="fa-crown" :text="role.role"></DetailCardWithIcon>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-3">
            <InfoCardWithForm title="Status" icon="fa-bookmark">
                <Dropdown v-model="project.status" :options="statusChoices" optionValue="value" @change="patchProject({ status: project.status })" optionLabel="label" class="w-full"></Dropdown>
            </InfoCardWithForm>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-3">
            <InfoCardWithForm title="Pin Project" icon="fa fa-thumbtack">
                <Checkbox :binary="true" v-model="project.pinned" @change="pinProject"></Checkbox>
            </InfoCardWithForm>
        </div>
    </div>

    <div class="grid">
        <div class="col-12 md:col-6 lg:col-6 xl:col-4">
            <LatestFindingsDashboard :project-id="this.projectId"></LatestFindingsDashboard>
            <DashboardFindingsCount></DashboardFindingsCount>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-4">
            <DashboardSeverityChart></DashboardSeverityChart>
        </div>
        <div class="col-12 md:col-6 lg:col-6 xl:col-4">
            <Card class="card">
                <template #title>Information</template>
                <template #content>
                    <div class="grid">
                        <div class="col-6">Test Method</div>
                        <div class="col-6">{{ project.test_method }}</div>
                    </div>
                    <div class="grid">
                        <div class="col-6">Company</div>
                        <div class="col-6">{{ project.company_name }}</div>
                    </div>
                    <div class="grid">
                        <div class="col-6">Pentest Types</div>
                        <div class="col-6">{{ getPentestTypeDisplay() }}</div>
                    </div>
                    <div class="grid">
                        <div class="col-6">Language</div>
                        <div class="col-6">{{ project.language }}</div>
                    </div>
                </template>
            </Card>

            <Card class="card">
                <template #title>Description</template>
                <template #content>
                    <div v-html="renderMarkdown(project.description)"></div>
                </template>
            </Card>
        </div>
    </div>
</template>
