<script setup>
import { cn } from '@/lib/utils';
import { DotsHorizontalIcon } from '@radix-icons/vue';

const props = defineProps({
    class: { type: null, required: false }
});
</script>

<template>
    <span :class="cn('flex h-9 w-9 items-center justify-center', props.class)" aria-hidden="true" role="presentation">
        <slot>
            <DotsHorizontalIcon class="h-4 w-4" />
        </slot>
        <span class="sr-only">More</span>
    </span>
</template>
