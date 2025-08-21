<script>
import Card from './Card.vue';

export default {
    name: 'InfoCardWithForm',
    components: { Card },
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
    <Card class="mb-0 pb-0 h-full">
        <div class="flex justify-between mb-3">
            <div>
                <span class="block text-muted-foreground font-medium mb-3">{{ title }}</span>
                <slot />
            </div>
            <div class="flex items-center justify-center text-muted-foreground" style="width: 2.5rem; height: 2.5rem">
                <i :class="icon" class="fa text-muted-foreground text-xl"></i>
            </div>
        </div>
    </Card>
</template>
