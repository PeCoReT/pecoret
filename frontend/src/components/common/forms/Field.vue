<script>
export default {
    name: "Field",
    props: {
        label: null,
    }
}
</script>

<template>
    <div class="flex flex-col">
        <div class="flex flex-col gap-2">
            <slot name="label">
                <label v-if="label !== null">{{ label }}</label>
            </slot>
            <slot></slot>
        </div>
    </div>
</template>
