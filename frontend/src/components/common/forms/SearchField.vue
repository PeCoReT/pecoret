<script>
export default {
    name: 'SearchField',
    props: {
        placeholder: "Search"
    }
};
</script>

<template>
    <div class="flex flex-col grow basis-0 gap-2">
        <slot name="label">
            <label v-if="label !== null">{{ label }}</label>
        </slot>
        <slot></slot>
    </div>
</template>

<style scoped></style>
