<script>
import Menubar from 'primevue/menubar';

export default {
    name: 'Navbar',
    components: {Menubar},
    props: {
        items: {
            required: false
        }
    }
};
</script>

<template>
    <Menubar :model="items" class="w-screen">
        <template #item="{ label, item, props, root, hasSubmenu }">
            <router-link v-if="item.route" :to="item.route" v-bind="props.action">
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
</template>

<style>
.router-link-exact-active {
    background-color: var(--p-surface-600);
    border-radius: inherit;
}
</style>