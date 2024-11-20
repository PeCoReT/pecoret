<script>
import { useAuthStore } from '@/store/auth';
import ProjectTabMenu from '@/components/navigation/ProjectTabMenu.vue';
import AttackSurfaceTabMenu from '@/components/navigation/AttackSurfaceTabMenu.vue';

export default {
    name: 'AppTopbar',
    data() {
        return {
            authStore: useAuthStore(),
            showLinks: {
                projects: ['isPentester', 'isAdmin', 'isManagement'],
                advisories: ['isPentester', 'isAdmin'],
                companies: ['isPentester', 'isAdmin', 'isManagement', 'isCustomer'],
                attackSurface: ['isPentester', 'isAdmin'],
                kbChecklists: ['isPentester', 'isAdmin', 'isManagement'],
                kbVulnTemplates: ['isPentester', 'isAdmin', 'isManagement']
            },
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
            if (this.checkShowLink('projects') === true) {
                items.push({
                    label: 'Projects',
                    route: this.$router.resolve({ name: 'ProjectList' })
                });
            }
            if (this.checkShowLink('companies') === true) {
                items.push({
                    label: 'Companies',
                    route: this.$router.resolve({ name: 'CompanyList' })
                });
            }
            if (this.checkShowLink('kbVulnTemplates') === true || this.checkShowLink('kbChecklists') === true) {
                let knowledgeItems = [];
                if (this.checkShowLink('kbVulnTemplates') === true) {
                    knowledgeItems.push({
                        label: 'Vulnerability Templates',
                        route: this.$router.resolve({ name: 'VulnerabilityTemplateList' })
                    });
                    knowledgeItems.push({
                        label: 'Technologies',
                        route: this.$router.resolve({ name: 'TechnologyList' })
                    });
                }
                if (this.checkShowLink('kbChecklists') === true) {
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
            if (this.checkShowLink('advisories') === true) {
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

            if (this.checkShowLink('attackSurface') === true) {
                items.push({
                    label: 'Attack Surface',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceSearch'
                    })
                });
            }

            if (this.authStore.groups.isAdmin === true) {
                items.push({
                    label: 'Admin Panel',
                    command: () => {
                        window.open('/admin/', '_blank');
                    }
                });
            }
            if (this.authStore.isAuthenticated) {
                let user = { label: this.authStore.me.username, items: [] };
                user.items = this.userMenuItems;
                items.push(user);
            }
            return items;
        }
    },
    methods: {
        checkShowLink(name) {
            return this.showLinks[name].some((attr) => this.authStore.groups[attr] === true);
        },
        onLogout() {
            this.$api.post(this.$api.e.authLogout).then(() => {
                this.authStore.unsetMe();

                this.$router.push({ name: 'Login' });
            });
        },
        isAttackSurfaceRoute() {
            if (this.$route.name && this.$route.name.startsWith('AttackSurface')) {
                return true;
            }
            return false;
        }
    },
    components: { AttackSurfaceTabMenu, ProjectTabMenu }
};
</script>

<template>
    <Menubar :model="items" class="h-16 w-full px-8 sm:px-8 transition-[left] duration-[var(--layout-section-transition-duration)] flex items-center !rounded-none" :pt="{ rootList: { class: 'w-full flex justify-end rounded-none' } }">
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
    <AttackSurfaceTabMenu v-else-if="isAttackSurfaceRoute()"></AttackSurfaceTabMenu>
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
