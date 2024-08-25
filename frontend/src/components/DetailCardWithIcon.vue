<script>
export default {
    name: 'DetailCardWithIcon',
    props: {
        title: {
            required: true
        },
        loading: {
            required: false,
            default: false
        },
        icon: {
            required: true
        },
        text: {
            required: true
        },
        styleClass: {
            default: 'h-full'
        }
    }
};
</script>

<template>
    <div :class="'card mb-0 ' + styleClass">
        <div class="flex justify-between mb-3">
            <div>
                <span class="block text-gray-500 font-medium mb-3">{{ title }}</span>
                <div v-if="loading === false" class="">{{ text }}</div>
                <div v-else class="text-gray-900 font-medium text-xl">
                    <Skeleton class="w-full"></Skeleton>
                </div>
            </div>
            <div class="flex items-center justify-center text-gray-500" style="width: 2.5rem; height: 2.5rem">
                <i class="fa text-secondary-800 text-xl" :class="icon"></i>
            </div>
        </div>
    </div>
</template>
