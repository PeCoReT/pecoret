<script setup>
import { toggleVariants } from '@/components/ui/toggle';
import { cn } from '@/lib/utils';
import { ToggleGroupItem, useForwardProps } from 'radix-vue';
import { computed, inject } from 'vue';

const props = defineProps({
    value: { type: String, required: true },
    defaultValue: { type: Boolean, required: false },
    pressed: { type: Boolean, required: false },
    disabled: { type: Boolean, required: false },
    asChild: { type: Boolean, required: false },
    as: { type: null, required: false },
    class: { type: null, required: false },
    variant: { type: null, required: false },
    size: { type: null, required: false }
});

const context = inject('toggleGroup');

const delegatedProps = computed(() => {
    const { class: _, variant, size, ...delegated } = props;
    return delegated;
});

const forwardedProps = useForwardProps(delegatedProps);
</script>

<template>
    <ToggleGroupItem
        :class="
            cn(
                toggleVariants({
                    variant: context?.variant || variant,
                    size: context?.size || size
                }),
                props.class
            )
        "
        v-bind="forwardedProps"
    >
        <slot />
    </ToggleGroupItem>
</template>
