<script setup>
import { cn } from '@/lib/utils';
import { Primitive } from 'radix-vue';
import { ReloadIcon } from '@radix-icons/vue';
import { buttonVariants } from '@/components/ui/button';

const props = defineProps({
    variant: { type: null, required: false },
    size: { type: null, required: false },
    class: { type: null, required: false },
    loading: { type: Boolean, required: true },
    asChild: { type: Boolean, required: false },
    as: { type: null, required: false, default: 'button' }
});
</script>

<template>
    <Primitive :as="as" :as-child="asChild" :class="cn(buttonVariants({ variant, size }), props.class)">
        <ReloadIcon class="animate-spin" v-if="loading === true"></ReloadIcon>
        <slot />
    </Primitive>
</template>
