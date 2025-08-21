<script>
export default {
    name: 'Form'
};
</script>

<template>
    <div class="flex flex-col md:flex-row space-y-4">
        <div class="md:w-full space-y-3">
            <slot></slot>
        </div>
    </div>
</template>
