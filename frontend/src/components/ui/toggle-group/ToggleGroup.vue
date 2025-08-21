<script setup>
import { cn } from '@/lib/utils';
import { ToggleGroupRoot, useForwardPropsEmits } from 'radix-vue';
import { computed, provide } from 'vue';

const props = defineProps({
    rovingFocus: { type: Boolean, required: false },
    disabled: { type: Boolean, required: false },
    orientation: { type: String, required: false },
    dir: { type: String, required: false },
    loop: { type: Boolean, required: false },
    asChild: { type: Boolean, required: false },
    as: { type: null, required: false },
    type: { type: null, required: false },
    modelValue: { type: null, required: false },
    defaultValue: { type: null, required: false },
    class: { type: null, required: false },
    variant: { type: null, required: false },
    size: { type: null, required: false }
});
const emits = defineEmits(['update:modelValue']);

provide('toggleGroup', {
    variant: props.variant,
    size: props.size
});

const delegatedProps = computed(() => {
    const { class: _, ...delegated } = props;
    return delegated;
});

const forwarded = useForwardPropsEmits(delegatedProps, emits);
</script>

<template>
    <ToggleGroupRoot :class="cn('flex items-center justify-center gap-1', props.class)" v-bind="forwarded">
        <slot />
    </ToggleGroupRoot>
</template>
