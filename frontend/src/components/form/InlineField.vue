<script>
export default {
    name: 'InlineField',
    props: {
        label: null
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
