<script setup>
import { cn } from '@/lib/utils';
import { ComboboxEmpty } from 'radix-vue';
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
</script>

<template>
    <ComboboxEmpty :class="cn('py-6 text-center text-sm', props.class)" v-bind="delegatedProps">
        <slot />
    </ComboboxEmpty>
</template>
