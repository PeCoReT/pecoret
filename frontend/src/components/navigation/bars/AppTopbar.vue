<script>
import { useAuthStore } from '@/store/auth';
import ProjectTabMenu from '@/components/navigation/ProjectTabMenu.vue';
import AuthService from '@/service/AuthService';

export default {
    name: 'AppTopbar',
    data() {
        return {
            authStore: useAuthStore(),
            userMenuItems: [
                {
                    label: 'API-Tokens',
                    icon: 'fa fa-fingerprint',
                    route: this.$router.resolve({
                        name: 'APITokenList'
                    })
                },
                {
                    label: 'Settings',
                    icon: 'fa fa-gear',
                    route: this.$router.resolve({
                        name: 'UserProfileSettings'
                    })
                },
                {
                    separator: true
                },
                {
                    label: 'Logout',
                    icon: 'fa fa-right-from-bracket',
                    command: this.onLogout
                }
            ]
        };
    },
    computed: {
        items() {
            let items = [];
            if (this.showProjectButton === true) {
                items.push({
                    label: 'Projects',
                    route: this.$router.resolve({ name: 'ProjectList' })
                });
            }
            if (this.showCompanyButton === true) {
                items.push({
                    label: 'Companies',
                    route: this.$router.resolve({ name: 'CompanyList' })
                });
            }
            if (this.showChecklistButton === true || this.showVulnerabilityTemplatesButton === true) {
                let knowledgeItems = [];
                if (this.showVulnerabilityTemplatesButton === true) {
                    knowledgeItems.push({
                        label: 'Vulnerability Templates',
                        route: this.$router.resolve({ name: 'VulnerabilityTemplateList' })
                    });
                    knowledgeItems.push({
                        label: 'Technologies',
                        route: this.$router.resolve({ name: 'TechnologyList' })
                    });
                }
                if (this.showChecklistButton === true) {
                    knowledgeItems.push({
                        label: 'Checklists',
                        items: [
                            {
                                label: 'Checklists',
                                route: this.$router.resolve({ name: 'ChecklistList' })
                            },
                            {
                                label: 'Categories',
                                route: this.$router.resolve({ name: 'ChecklistCategoryList' })
                            }
                        ]
                    });
                }
                items.push({
                    label: 'Knowledge Base',
                    items: knowledgeItems
                });
            }
            if (this.showAdvisoriesButton === true) {
                let advisories = {
                    label: 'Advisories',
                    items: [
                        {
                            label: 'Dashboard',
                            route: this.$router.resolve({ name: 'AdvisoryDashboard' })
                        },
                        {
                            label: 'Advisory List',
                            route: this.$router.resolve({ name: 'AdvisoryList' })
                        },
                        {
                            label: 'Labels',
                            route: this.$router.resolve({ name: 'AdvisoryLabelList' })
                        }
                    ]
                };
                items.push(advisories);
            }

            if (this.showASMonitorButton === true) {
                items.push({
                    label: 'Attack Surface',
                    items: [
                        {
                            label: 'Programs',
                            route: this.$router.resolve({
                                name: 'AttackSurfaceProgramList'
                            })
                        },
                        {
                            label: 'Targets',
                            route: this.$router.resolve({
                                name: 'AttackSurfaceTargetList'
                            })
                        },
                        {
                            label: 'Ports',
                            route: this.$router.resolve({
                                name: 'AttackSurfacePortList'
                            })
                        },
                        {
                            label: 'URLs',
                            route: this.$router.resolve({
                                name: 'AttackSurfaceURLList'
                            })
                        },
                        {
                            label: 'Scan Findings',
                            route: this.$router.resolve({
                                name: 'AttackSurfaceScanFindingList'
                            })
                        },
                        {
                            label: 'Tags',
                            route: this.$router.resolve({
                                name: 'AttackSurfaceTagList'
                            })
                        }
                    ]
                });
            }

            if (this.authStore.groups.isAdmin === true) {
                items.push({
                    label: 'Admin Panel',
                    items: [
                        {
                            label: 'Users',
                            route: this.$router.resolve({
                                name: 'UserList'
                            })
                        },
                        {
                            label: 'Project Types',
                            route: this.$router.resolve({
                                name: 'ProjectTypeList'
                            })
                        },
                        {
                            label: 'Settings',
                            route: this.$router.resolve({
                                name: 'AdminSettings'
                            })
                        }
                    ]
                });
            }
            if (this.authStore.isAuthenticated) {
                let user = { label: this.authStore.me.username, items: [] };
                user.items = this.userMenuItems;
                items.push(user);
            }
            return items;
        },

        showCompanyButton() {
            if (this.authStore.groups.isVendor === true) {
                return false;
            }
            return true;
        },
        showVulnerabilityTemplatesButton() {
            if (this.authStore.groups.isVendor === true || this.authStore.groups.isCustomer === true) {
                return false;
            }
            return true;
        },
        showChecklistButton() {
            if (this.authStore.groups.isPentester === true) {
                return true;
            }
            return false;
        },
        showProjectButton() {
            if (this.authStore.groups.isVendor === true) {
                return false;
            }
            return true;
        },
        showAdvisoriesButton() {
            if (this.authStore.groups.isCustomer === true) {
                return false;
            }
            return true;
        },
        showASMonitorButton() {
            if (this.authStore.groups.isPentester === true) {
                return true;
            }
            return false;
        }
    },
    methods: {
        onLogout() {
            const authService = new AuthService();
            authService.logout(this.$api).then(() => {
                this.$router.push({ name: 'Login' });
            });
        }
    },
    components: { ProjectTabMenu }
};
</script>

<template>
    <Menubar :model="items" class="layout-topbar !rounded-none" :pt="{ rootList: { class: 'w-full flex justify-end rounded-none' } }">
        <template #start>
            <router-link to="/" class="">
                <img src="/images/logo-no-slogan.svg" alt="logo" class="max-w-[10rem] md:max-h-[3rem]" />
            </router-link>
        </template>
        <template #item="{ label, item, props, root, hasSubmenu }">
            <router-link class="flex items-center" v-bind="props.action" :to="item.route" v-if="item.route">
                <span v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
            </router-link>
            <a v-else :href="item.url" :target="item.target" v-bind="props.action">
                <span v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
                <span :class="[hasSubmenu && (root ? 'fa fa-chevron-down' : 'fa fa-chevron-down')]" v-bind="props.submenuicon" />
            </a>
        </template>
    </Menubar>
    <ProjectTabMenu v-if="this.$route.params.projectId"></ProjectTabMenu>
</template>

<style>
.p-menubar-submenu {
    right: 0 !important; /* Align the dropdown to the right */
    left: auto !important; /* Ensure the left property is not overriding */
    position: absolute !important; /* Ensure the dropdown is positioned correctly */
}

.p-menubar-item {
    position: relative; /* Ensure the dropdown item is positioned correctly */
}
</style>
