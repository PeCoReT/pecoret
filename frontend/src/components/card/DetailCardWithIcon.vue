<script>
import Card from './Card.vue';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';

export default {
    name: 'DetailCardWithIcon',
    components: { DefaultSkeleton, Card },
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
    <Card :class="'mb-0 pb-0 ' + styleClass">
        <div class="flex justify-between mb-3">
            <div>
                <span class="block text-muted-foreground font-medium mb-3">{{ title }}</span>
                <div v-if="loading === false" class="">{{ text }}</div>
                <div v-else class="text-primary-foreground font-medium text-xl">
                    <DefaultSkeleton class="w-full"></DefaultSkeleton>
                </div>
            </div>
            <div class="flex items-center justify-center text-muted-foreground" style="width: 2.5rem; height: 2.5rem">
                <i :class="icon" class="fa text-muted-foreground text-xl"></i>
            </div>
        </div>
    </Card>
</template>
