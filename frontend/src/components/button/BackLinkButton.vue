<script>
import { Button } from '@/components/ui/button';

export default {
    name: 'BackLinkButton',
    components: { Button },
    props: {
        href: {
            required: true
        },
        text : {
            required: true
        }
    }
};
</script>

<template>
    <Button
        variant="link"
        size="small"
        as="a"
        :href="href"
    >
        <i class="fa fa-arrow-left"></i> {{ text }}
    </Button>
</template>

