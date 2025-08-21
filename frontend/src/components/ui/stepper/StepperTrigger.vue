<script setup>
import { cn } from '@/lib/utils';
import { StepperTrigger, useForwardProps } from 'radix-vue';

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
    <StepperTrigger :class="cn('p-1 flex flex-col items-center text-center gap-1 rounded-md', props.class)" v-bind="forwarded">
        <slot />
    </StepperTrigger>
</template>
