<script>
export default {
    name: 'TechnologyBadge',
    props: {
        technologyName: {
            required: true
        },
        disableHover: {
            default: false
        }
    },
    computed: {
        badgeClasses() {
            return {
                'bg-surface-950 text-white text-sm px-2 py-1 rounded border border-gray-800': true,
                'hover:bg-surface-800 hover:cursor-pointer': !this.disableHover
            };
        }
    }
};
</script>

<template>
    <span :class="badgeClasses">{{ technologyName }}</span>
</template>
