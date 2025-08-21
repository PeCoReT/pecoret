<script setup>
import { cn } from '@/lib/utils';
import { Toggle, useForwardPropsEmits } from 'radix-vue';
import { computed } from 'vue';
import { toggleVariants } from '.';

const props = defineProps({
    defaultValue: { type: Boolean, required: false },
    pressed: { type: Boolean, required: false },
    disabled: { type: Boolean, required: false, default: false },
    asChild: { type: Boolean, required: false },
    as: { type: null, required: false },
    class: { type: null, required: false },
    variant: { type: null, required: false, default: 'default' },
    size: { type: null, required: false, default: 'default' }
});

const emits = defineEmits(['update:pressed']);

const delegatedProps = computed(() => {
    const { class: _, size, variant, ...delegated } = props;

    return delegated;
});

const forwarded = useForwardPropsEmits(delegatedProps, emits);
</script>

<template>
    <Toggle :class="cn(toggleVariants({ variant, size }), props.class)" v-bind="forwarded">
        <slot />
    </Toggle>
</template>
