<script>
import { useAuthStore } from '@/store/auth';
import ProjectTabMenu from './ProjectTabMenu.vue';
import AuthService from '../service/AuthService';

export default {
    name: 'AppTopbar',
    data() {
        return {
            topbarMenuActive: null,
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
                        name: 'UserSettingsDetail'
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
            if (this.showChecklistButton === true) {
                items.push({
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
            if (this.showVulnerabilityTemplatesButton === true) {
                items.push({
                    label: 'Vulnerability Templates',
                    route: this.$router.resolve({ name: 'VulnerabilityTemplateList' })
                });
            }
            if (this.showAdvisoriesButton === true) {
                let advisories = { label: 'Advisories', items: [] };
                advisories.items.push({
                    label: 'My Advisories',
                    route: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                });
                if (this.authStore.groups.isAdvisoryManagement === true) {
                    advisories.items.push({
                        label: 'Dashboard',
                        route: this.$router.resolve({
                            name: 'AdvisoryManagementDashboard'
                        })
                    });
                    advisories.items.push({
                        label: 'Labels',
                        route: this.$router.resolve({
                            name: 'AdvisoryManagementLabelList'
                        })
                    });
                }
                items.push(advisories);
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
                            label: 'Report Templates',
                            route: this.$router.resolve({
                                name: 'ReportTemplateList'
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
        topbarMenuClasses() {
            return {
                'layout-topbar-menu-mobile-active': this.topbarMenuActive
            };
        }
    },
    methods: {
        onLogout() {
            const authService = new AuthService();
            authService.logout(this.$api).then(() => {
                this.$router.push({ name: 'Login' });
            });
        },
        toggleMenu() {
            this.topbarMenuActive = !this.topbarMenuActive;
        }
    },
    components: { ProjectTabMenu }
};
</script>

<template>
    <Menubar :model="items" class="surface-card layout-topbar" ref="menu" :pt="{ menu: { class: 'top-menu' } }">
        <template #start>
            <router-link to="/" class="layout-topbar-logo">
                <img src="/images/logo-no-slogan.svg" alt="logo" />
            </router-link>
        </template>
        <template #item="{ label, item, props, root, hasSubmenu }">
            <router-link class="flex" v-bind="props.action" v-slot="routerProps" :to="item.route" v-if="item.route">
                <span v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
            </router-link>
            <a v-else :href="item.url" :target="item.target" v-bind="props.action">
                <span v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
                <span :class="[hasSubmenu && (root ? 'pi pi-fw pi-angle-down' : 'pi pi-fw pi-angle-right')]" v-bind="props.submenuicon" />
            </a>
        </template>
    </Menubar>
    <ProjectTabMenu v-if="this.$route.params.projectId"></ProjectTabMenu>
</template>
