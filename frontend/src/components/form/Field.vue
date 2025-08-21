<script>
import { Label } from '@/components/ui/label';

export default {
    name: 'Field',
    components: { Label },
    props: {
        label: null
    }
};
</script>

<template>
    <div class="flex flex-col">
        <div class="flex flex-col gap-2">
            <slot name="label">
                <Label v-if="label !== null">{{ label }}</Label>
            </slot>
            <slot></slot>
        </div>
    </div>
</template>
