<script>
import { Badge } from '@/components/badge';

export default {
    name: 'ScopeBadge',
    components: { Badge },
    props: {
        scope: {
            required: true
        }
    },
    computed: {
        color() {
            if (this.scope === 'In Scope') {
                return '#4CAF50';
            } else if (this.scope === 'Undefined') {
                return '#9E9E9E';
            } else {
                return '#F44336';
            }
        }
    }
};
</script>

<template>
    <Badge :color="color" :text="scope"></Badge>
</template>
