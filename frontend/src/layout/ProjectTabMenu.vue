<script>
import { useAuthStore } from '@/store/auth';
import ProjectService from '@/service/ProjectService';

export default {
    name: 'ProjectTabMenu',
    mounted() {
        if (!this.authStore.activeProject.name) {
            this.projectService.getProject(this.$route.params.projectId).then((response) => {
                this.authStore.activateProject(response.data);
            });
        }
    },
    data() {
        return {
            authStore: useAuthStore(),
            projectService: new ProjectService(),
            items: [
                {
                    label: 'Dashboard',
                    icon: 'fa fa-chart-line',
                    route: this.$router.resolve({
                        name: 'ProjectDetail',
                        params: { projectId: this.$route.params.projectId }
                    }).path
                },
                {
                    label: 'Findings',
                    icon: 'fa fa-bug',
                    route: this.$router.resolve({
                        name: 'FindingList',
                        params: { projectId: this.$route.params.projectId }
                    }).path
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
                    items: [
                        {
                            label: 'Web Applications',
                            route: this.$router.resolve({
                                name: 'WebApplicationList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            }).path
                        },
                        {
                            label: 'Hosts',
                            route: this.$router.resolve({
                                name: 'HostList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            }).path
                        },
                        {
                            label: 'Services',
                            route: this.$router.resolve({
                                name: 'ServiceList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            }).path
                        },
                        {
                            label: 'Mobile Applications',
                            route: this.$router.resolve({
                                name: 'MobileApplicationList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        },
                        {
                            label: 'Thick Clients',
                            route: this.$router.resolve({
                                name: 'ThickClientList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        },
                        {
                            label: 'Generic',
                            route: this.$router.resolve({
                                name: 'GenericAssetList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        }
                    ]
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
    <Menubar :model="items" class="surface-card">
        <template #item="{ label, item, props, root, hasSubmenu }">
            <router-link v-if="item.route" v-slot="routerProps" :to="item.route">
                <span v-bind="props.action">
                    <span v-bind="props.icon" />
                    <span v-bind="props.label">{{ label }}</span>
                </span>
            </router-link>
            <a v-else :href="item.url" :target="item.target" v-bind="props.action">
                <span v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
                <span :class="[hasSubmenu && (root ? 'pi pi-fw pi-angle-down' : 'pi pi-fw pi-angle-right')]" v-bind="props.submenuicon" />
            </a>
        </template>
    </Menubar>
</template>
