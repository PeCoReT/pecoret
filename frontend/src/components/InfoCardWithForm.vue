<script>
export default {
    name: 'InfoCardWithForm',
    props: {
        title: {
            required: true
        },
        icon: {
            required: true
        }
    }
};
</script>

<template>
<div class="card mb-0 h-full">
    <div class="flex justify-between mb-3">
        <div>
            <span class="block text-gray-500 font-medium mb-3">{{ title }}</span>
            <slot />
        </div>
        <div class="flex items-center justify-center text-gray-500" style="width: 2.5rem; height: 2.5rem;">
            <i class="fa text-secondary-800 text-xl" :class="icon"></i>
        </div>
    </div>
</div>

</template>
