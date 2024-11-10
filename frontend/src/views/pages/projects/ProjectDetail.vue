<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import ProjectUpdateDialog from '@/components/dialogs/ProjectUpdateDialog.vue';
import markdown from '@/utils/markdown';
import DashboardSeverityChart from '@/components/projects/DashboardSeverityChart.vue';
import DashboardFindingsCount from '@/components/projects/DashboardFindingsCount.vue';
import LatestFindingsDashboard from '@/components/projects/LatestFindingsDashboard.vue';

export default {
    name: 'ProjectDetail',
    data() {
        return {
            projectId: this.$route.params.projectId,
            project: { company: {} },
            role: {},
            updatedSuccessToastTitle: 'Project updated!',
            updatedSuccessToastText: 'Project was updated successfully!',
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
    },
    methods: {
        getProject() {
            this.$api.get(this.$api.e.projectDetail, { pk: this.projectId }).then((response) => {
                this.project = response.data;
                this.getMembership();
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
            if (this.project.visibility === 'Pentesters') {
                this.role = { role: 'Public Pentester' };
                return;
            }
            this.$api.get(this.$api.e.projectMembershipsMe, { pk: this.projectId }).then((response) => {
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
            this.$api.patch(this.$api.e.projectDetail, { pk: this.projectId }, data).then((response) => {
                this.project = response.data;
                this.$toast.add({
                    severity: 'success',
                    summary: this.updatedSuccessToastTitle,
                    life: 3000,
                    detail: this.updatedSuccessToastText
                });
            });
        },
        pinProject() {
            let resp;
            if (this.project.pinned === true) {
                resp = this.$api.post(this.$api.e.projectsPinProject, { pk: this.projectId });
            } else {
                resp = this.$api.delete(this.$api.e.projectsUnpinProject, { pk: this.projectId });
            }
            resp.then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: this.updatedSuccessToastTitle,
                    life: 3000,
                    detail: this.updatedSuccessToastText
                });
            });
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
        <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
    </div>

    <div class="grid mt-3">
        <div class="flex justify-end">
            <ProjectUpdateDialog :project="project" @object-updated="getProject"></ProjectUpdateDialog>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mt-3">
        <div class="col-span-1">
            <DetailCardWithIcon title="Dates" :text="projectDateDisplay" icon="fa-calendar"></DetailCardWithIcon>
        </div>
        <div class="col-span-1">
            <DetailCardWithIcon title="Role" icon="fa-crown" :text="role.role || 'Unknown'"></DetailCardWithIcon>
        </div>
        <div class="col-span-1">
            <InfoCardWithForm title="Status" icon="fa-bookmark">
                <Select v-model="project.status" :options="statusChoices" optionValue="value" @change="patchProject({ status: project.status })" optionLabel="label" class="w-full"></Select>
            </InfoCardWithForm>
        </div>
        <div class="col-span-1">
            <InfoCardWithForm title="Pin Project" icon="fa fa-thumbtack">
                <Checkbox :binary="true" v-model="project.pinned" @change="pinProject"></Checkbox>
            </InfoCardWithForm>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mt-3">
        <div class="col-span-1">
            <LatestFindingsDashboard :project-id="this.projectId"></LatestFindingsDashboard>
            <DashboardFindingsCount></DashboardFindingsCount>
        </div>
        <div class="col-span-1">
            <DashboardSeverityChart></DashboardSeverityChart>
        </div>
        <div class="col-span-1">
            <Card class="card">
                <template #title>Information</template>
                <template #content>
                    <div class="grid grid-cols-2 gap-4">
                        <div>Test Method</div>
                        <div>{{ project.test_method }}</div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>Company</div>
                        <div>{{ project.company.name }}</div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>Pentest Types</div>
                        <div>{{ getPentestTypeDisplay() }}</div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>Language</div>
                        <div>{{ project.language }}</div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>Visibility</div>
                        <div>{{ project.visibility }}</div>
                    </div>
                </template>
            </Card>

            <Card class="card">
                <template #title>Description</template>
                <template #content>
                    <div v-html="renderMarkdown(project.description)" class="markdown-block"></div>
                </template>
            </Card>
        </div>
    </div>
</template>
