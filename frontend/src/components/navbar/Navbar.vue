<template>
    <nav class="bg-navbar text-navbar-foreground p-1 border">
        <div class="flex justify-between items-center">
            <button @click="toggleMenu" class="md:hidden">
                <i class="fa fa-bars text-xl"></i>
            </button>
            <ul :class="{ hidden: !isMenuOpen, flex: isMenuOpen }" class="flex-col md:flex md:flex-row md:items-center w-full md:w-auto mt-4 md:mt-0">
                <li v-for="item in items" :key="item.label" class="relative" @click.stop="toggleSubmenu(item)">
                    <router-link class="flex items-center h-full py-2 px-4 hover:bg-accent rounded-lg transition cursor-pointer" :to="item.route" v-if="item.route">
                        <i :class="item.icon" class="mr-2"></i>
                        <span>{{ item.label }}</span>
                    </router-link>
                    <span v-else class="flex items-center h-full py-2 px-4 hover:bg-accent rounded-lg transition cursor-pointer">
                        <i :class="item.icon" class="mr-2"></i>
                        <span>{{ item.label }}</span>
                        <i v-if="item.items" class="ml-2 fa fa-chevron-down"></i>
                    </span>
                    <ul v-if="item.items && item.isOpen" class="absolute bg-popover text-popover-foreground mt-2 rounded shadow-lg z-10 w-full border">
                        <li v-for="subItem in item.items" :key="subItem.label" class="w-full h-full" @click.stop="closeAllSubmenus()">
                            <router-link v-if="subItem.route" :to="subItem.route" class="w-full h-full block py-2 px-4 hover:bg-accent hover:text-accent-foreground rounded transition hover:cursor-pointer">
                                <i :class="subItem.icon" class="mr-2"></i>
                                <span>{{ subItem.label }}</span>
                            </router-link>
                            <span v-else>
                                <i :class="subItem.icon" class="mr-2"></i>
                                <span>{{ subItem.label }}</span>
                            </span>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'ResponsiveNavbar',
    props: {
        items: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            isMenuOpen: false
        };
    },
    methods: {
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
        handleClick(event) {
            this.closeAllSubmenus();
        }
    },
    mounted() {
        // Initialize the isOpen property for items with submenus
        this.items.forEach((item) => {
            if (item.items) {
                item.isOpen = false;
            }
        });
        document.addEventListener('click', this.handleClick);
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClick);
    }
};
</script>
