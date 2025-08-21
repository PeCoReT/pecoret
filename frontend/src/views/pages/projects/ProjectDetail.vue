<script>
import { DashboardFindingsCount, DashboardSeverityChart, LatestFindingsDashboard } from '@/partials/projects';
import { DetailCardWithIcon, InfoCardWithForm } from '@/components/card';
import { Button } from '@/components/ui/button';
import { Select } from '@/components/select';
import { Checkbox } from '@/components/ui/checkbox';

export default {
    name: 'ProjectDetail',
    data() {
        return {
            projectId: this.$route.params.projectId,
            project: { company: {} },
            role: {},
            updatedSuccessToastTitle: 'Project updated!',
            updatedSuccessToastText: 'Project was updated successfully!',
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
            });
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
            if (!this.project.project_types) {
                return '';
            }
            let pentestTypeNames = [];
            this.project.project_types.forEach((element) => {
                pentestTypeNames.push(element.name);
            });
            return pentestTypeNames.join(', ');
        },
        patchProject(data) {
            this.$api.patch(this.$api.e.projectDetail, { pk: this.projectId }, data).then((response) => {
                this.project = response.data;
                this.$toaster({
                    title: this.updatedSuccessToastTitle,
                    duration: 3000,
                    description: this.updatedSuccessToastText
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
                this.$toaster({
                    title: this.updatedSuccessToastTitle,
                    duration: 3000,
                    description: this.updatedSuccessToastText
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
        InfoCardWithForm,
        DashboardSeverityChart,
        Button,
        Select,
        Checkbox
    }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="flex justify-end">
            <Button as-child variant="outline">
                <a :href="this.$router.resolve({ name: 'ProjectUpdate', params: { projectId: this.projectId } }).href"> <i class="fa fa-edit"></i> Edit </a>
            </Button>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mt-3">
        <div class="col-span-1">
            <DetailCardWithIcon :text="projectDateDisplay" icon="fa-calendar" title="Dates"></DetailCardWithIcon>
        </div>
        <div class="col-span-1">
            <DetailCardWithIcon :text="role.role || 'Unknown'" icon="fa-crown" title="Role"></DetailCardWithIcon>
        </div>
        <div class="col-span-1">
            <InfoCardWithForm icon="fa-bookmark" title="Status">
                <Select v-model="project.status" :options="statusChoices" class="w-full" @update:modelValue="patchProject({ status: project.status })"></Select>
            </InfoCardWithForm>
        </div>
        <div class="col-span-1">
            <InfoCardWithForm icon="fa fa-thumbtack" title="Pin Project">
                <div class="flex items-center space-x-2">
                    <Checkbox v-model:checked="project.pinned" @update:checked="pinProject"></Checkbox>
                </div>
            </InfoCardWithForm>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mt-3">
        <div class="col-span-1">
            <LatestFindingsDashboard :project-id="this.projectId"></LatestFindingsDashboard>
            <DashboardFindingsCount class="mt-3"></DashboardFindingsCount>
        </div>
        <div class="col-span-1">
            <DashboardSeverityChart></DashboardSeverityChart>
        </div>
        <div class="col-span-1">
            <Card title="Information">
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
            </Card>

            <Card class="mt-3" title="Description">
                <div class="markdown-block" v-html="project.description_md"></div>
            </Card>
        </div>
    </div>
</template>
