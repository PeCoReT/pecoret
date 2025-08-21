<script setup>
import { cn } from '@/lib/utils';
import { ChevronDownIcon } from '@radix-icons/vue';
import { SelectScrollDownButton, useForwardProps } from 'radix-vue';
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

const forwardedProps = useForwardProps(delegatedProps);
</script>

<template>
    <SelectScrollDownButton :class="cn('flex cursor-default items-center justify-center py-1', props.class)" v-bind="forwardedProps">
        <slot>
            <ChevronDownIcon />
        </slot>
    </SelectScrollDownButton>
</template>
