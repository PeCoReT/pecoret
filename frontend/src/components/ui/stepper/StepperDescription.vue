<script setup>
import { cn } from '@/lib/utils';
import { StepperDescription, useForwardProps } from 'radix-vue';

import { computed } from 'vue';

const props = defineProps({
    asChild: { type: Boolean, required: false },
    as: { type: null, required: false },
    class: { type: null, required: false }
});

const delegatedProps = computed(() => {
    const { class: _, ...delegated } = props;

    return delegated;
});

const forwarded = useForwardProps(delegatedProps);
</script>

<template>
    <StepperDescription v-slot="slotProps" :class="cn('text-xs text-muted-foreground', props.class)" v-bind="forwarded">
        <slot v-bind="slotProps" />
    </StepperDescription>
</template>
