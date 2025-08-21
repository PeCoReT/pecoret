<script setup>
import { cn } from '@/lib/utils';

const props = defineProps({
    class: { type: null, required: false }
});
</script>

<template>
    <span :class="cn('font-normal text-foreground', props.class)" aria-current="page" aria-disabled="true" role="link">
        <slot />
    </span>
</template>
