<script>
import { useAuthStore } from '@/store/auth';
import ProjectTabMenu from '@/partials/projects/ProjectTabMenu.vue';
import { AttackSurfaceTabMenu } from '@/partials/attack_surface';
import KnowledgeBaseTabMenu from '@/partials/knowledgebase/KnowledgeBaseTabMenu.vue';
import AdvisorySubMenu from '@/partials/advisories/AdvisorySubMenu.vue';

export default {
    name: 'AppTopbar',
    components: { AdvisorySubMenu, KnowledgeBaseTabMenu, AttackSurfaceTabMenu, ProjectTabMenu },
    data() {
        return {
            isMenuOpen: false,
            items: [],
            authStore: useAuthStore(),
            showLinks: {
                projects: ['isPentester', 'isAdmin', 'isManagement'],
                advisories: ['isPentester', 'isAdmin'],
                companies: ['isPentester', 'isAdmin', 'isManagement', 'isCustomer'],
                attackSurface: ['isPentester', 'isAdmin'],
                knowledgeBase: ['isPentester', 'isAdmin', 'isManagement']
            },
            userMenuItems: [
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

    methods: {
        permissionedMenuItems() {
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
            if (this.checkShowLink('knowledgeBase')) {
                items.push({
                    label: 'Knowledge Base',
                    route: this.$router.resolve({ name: 'VulnerabilityTemplateList' })
                });
            }

            if (this.checkShowLink('advisories') === true) {
                let advisories = {
                    label: 'Advisories',
                    route: this.$router.resolve({ name: 'AdvisoryDashboard' })
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
        },
        toggleMenu() {
            this.isMenuOpen = !this.isMenuOpen;
        },
        toggleSubmenu(clickedItem) {
            this.closeAllSubmenus();
            clickedItem.isOpen = !clickedItem.isOpen;
        },
        closeAllSubmenus() {
            this.items.forEach((item) => {
                if (item.items) {
                    item.isOpen = false;
                }
            });
        },
        checkShowLink(name) {
            return this.showLinks[name].some((attr) => this.authStore.groups[attr] === true);
        },

        handleClick(event) {
            this.closeAllSubmenus();
        },
        isAttackSurfaceRoute() {
            if (this.$route.name && this.$route.name.startsWith('AttackSurface')) {
                return true;
            }
            return false;
        },
        onLogout() {
            this.$api.delete(this.$api.e.authLogout).then(() => {
                this.authStore.unsetMe();
                this.$router.push({ name: 'Home' });
            });
        },
        activeStateClass(item) {
            if (this.$route.path && item.route && this.$route.path.startsWith(item.route.path)) {
                return 'bg-accent';
            }
            return '';
        }
    },
    watch: {
        'authStore.isAuthenticated': {
            handler() {
                this.items = this.permissionedMenuItems();
            }
        }
    },
    mounted() {
        this.items = this.permissionedMenuItems();
        document.addEventListener('click', this.handleClick);
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClick);
    }
};
</script>

<template>
    <nav class="bg-navbar p-2 px-4 border text-navbar-foreground" v-if="authStore.isAuthenticated === true">
        <div class="flex justify-between items-center">
            <!-- Logo -->
            <div class="logo">
                <img src="/images/logo-no-slogan.svg" alt="Logo" class="h-4" />
            </div>
            <!-- Menu Button for Mobile -->
            <button @click="toggleMenu" class="md:hidden">
                <i class="fa fa-bars text-xl"></i>
            </button>
            <!-- Navigation Items -->
            <ul :class="{ hidden: !isMenuOpen, flex: isMenuOpen }" class="flex-col md:flex md:flex-row md:items-center w-full md:w-auto mt-4 md:mt-0">
                <li v-for="item in items" :key="item.label" class="relative" @click.stop="toggleSubmenu(item)">
                    <router-link v-if="item.route" :to="item.route" class="flex items-center py-2 px-4 hover:bg-accent rounded-lg transition cursor-pointer" :class="[activeStateClass(item)]">
                        <i :class="item.icon" class="mr-2" v-if="item.icon"></i>
                        <span>{{ item.label }}</span>
                    </router-link>
                    <span v-else-if="item.command" @click="item.command" class="w-full block py-2 px-4 hover:bg-accent rounded-lg transition hover:cursor-pointer">
                        {{ item.label }}
                    </span>
                    <span v-else class="flex items-center py-2 px-4 hover:bg-accent rounded-lg transition cursor-pointer" :class="[activeStateClass(item)]">
                        <i :class="item.icon" class="mr-2"></i>
                        <span>{{ item.label }}</span>
                        <i v-if="item.items" class="ml-2 fa fa-chevron-down"></i>
                    </span>

                    <ul v-if="item.items && item.isOpen" class="absolute right-0 top-full mt-2 min-w-[12rem] md:min-w-[14rem] border rounded shadow-lg z-50 bg-popover text-popover-foreground whitespace-nowrap">
                        <li v-for="subItem in item.items" :key="subItem.label" class="w-full" @click.stop="closeAllSubmenus()">
                            <router-link v-if="subItem.route" :to="subItem.route" class="w-full block py-2 px-4 hover:bg-accent rounded transition hover:cursor-pointer">
                                <i :class="subItem.icon" class="mr-2"></i>
                                <span>{{ subItem.label }}</span>
                            </router-link>
                            <span v-else-if="subItem.separator === true"><hr /></span>
                            <span
                                v-else-if="subItem.command"
                                class="w-full block py-2 px-4 hover:bg-accent rounded transition hover:cursor-pointer"
                                @click="
                                    () => {
                                        console.log(subItem.command);
                                        subItem['command']();
                                    }
                                "
                            >
                                <i :class="subItem.icon" class="mr-2"></i>
                                <span>{{ subItem.label }}</span>
                            </span>
                            <span v-else class="w-full block py-2 px-4 hover:bg-accent rounded transition hover:cursor-pointer">
                                <i :class="subItem.icon" class="mr-2"></i>
                                <span>{{ subItem.label }}</span>
                            </span>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </nav>
    <ProjectTabMenu v-if="this.$route.params.projectId"></ProjectTabMenu>
    <KnowledgeBaseTabMenu v-else-if="this.$route.path.includes('knowledge-base')"></KnowledgeBaseTabMenu>
    <AdvisorySubMenu v-else-if="this.$route.path.includes('advisories')"></AdvisorySubMenu>
    <AttackSurfaceTabMenu v-else-if="isAttackSurfaceRoute()"></AttackSurfaceTabMenu>
</template>
