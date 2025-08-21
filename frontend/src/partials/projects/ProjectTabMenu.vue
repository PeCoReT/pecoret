<script>
import { useAuthStore } from '@/store/auth';
import { Navbar } from '@/components/navbar';

export default {
    name: 'ProjectTabMenu',
    components: { Navbar },
    mounted() {
        if (!this.authStore.activeProject.name) {
            this.$api.get(this.$api.e.projectDetail, { pk: this.$route.params.projectId }).then((response) => {
                this.authStore.activateProject(response.data);
            });
        }
    },
    data() {
        return {
            authStore: useAuthStore(),
            items: [
                {
                    label: 'Dashboard',
                    icon: 'fa fa-chart-line',
                    route: this.$router.resolve({
                        name: 'ProjectDetail',
                        params: { projectId: this.$route.params.projectId }
                    })
                },
                {
                    label: 'Findings',
                    icon: 'fa fa-bug',
                    route: this.$router.resolve({
                        name: 'FindingList',
                        params: { projectId: this.$route.params.projectId }
                    })
                },
                {
                    label: 'Checklists',
                    icon: 'fa fa-circle-check',
                    route: this.$router.resolve({
                        name: 'ProjectChecklistList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Assets',
                    icon: 'fa fa-crosshairs',
                    route: this.$router.resolve({
                        name: 'AssetList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Reports',
                    icon: 'fa fa-file',
                    route: this.$router.resolve({
                        name: 'ReportList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Management',
                    icon: 'fa fa-calendar',
                    items: [
                        {
                            label: 'Contributors',
                            route: this.$router.resolve({
                                name: 'ContributorList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        },
                        {
                            label: 'User Accounts',
                            route: this.$router.resolve({
                                name: 'UserAccountList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        },
                        {
                            label: 'Contacts',
                            route: this.$router.resolve({
                                name: 'ContactList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        },
                        {
                            label: 'Files',
                            route: this.$router.resolve({
                                name: 'ProjectFileList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        }
                    ]
                },
                {
                    label: 'Vulnerabilities',
                    icon: 'fa fa-bolt',
                    route: this.$router.resolve({
                        name: 'VulnerabilityList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Commands',
                    icon: 'fa fa-terminal',
                    route: this.$router.resolve({
                        name: 'ProjectCommandList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Scopes',
                    icon: 'fa fa-star',
                    route: this.$router.resolve({
                        name: 'ProjectScopeList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Notes',
                    icon: 'fa fa-note-sticky',
                    route: this.$router.resolve({
                        name: 'ProjectNoteList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                }
            ]
        };
    }
};
</script>

<template>
    <Navbar :items="items"></Navbar>
</template>
