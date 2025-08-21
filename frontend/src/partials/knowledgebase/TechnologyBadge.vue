<script>
export default {
    name: "TechnologyBadge",
    props: {
        technology: {
            required: false
        }
    }
}
</script>

<template>
    <span class="bg-accent text-accent-foreground text-xs px-2 py-1 mt-2 rounded-lg border border-input hover:bg-secondary hover:cursor-pointer">
        {{ technology.name }}
    </span>
</template>
