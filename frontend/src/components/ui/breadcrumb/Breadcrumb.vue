<script setup>
const props = defineProps({
    class: { type: null, required: false }
});
</script>

<template>
    <nav :class="props.class" aria-label="breadcrumb">
        <slot />
    </nav>
</template>
