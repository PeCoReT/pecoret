<script>
export default {
    name: 'Timeline',
    props: {
        items: {
            type: Array,
            required: true
        }
    },
    emits: ['delete'],
    methods: {
        handleTitleClick(item) {
            this.$emit('delete', item);
        }
    }
};
</script>

<template>
    <ol class="relative border-s border-border">
        <li v-for="(item, idx) in items" :key="item.id ?? idx" class="mb-10 ms-4 last:mb-0">
            <div class="absolute w-3 h-3 rounded-full mt-1.5 -start-1.5 border border-border bg-accent"></div>

            <time class="mb-1 text-sm font-normal leading-none text-muted-foreground">
                {{ item.date }}
            </time>

            <h3 class="text-lg font-semibold text-muted-foreground cursor-pointer hover:underline transition-colors" @click="handleTitleClick(item.pk)">
                {{ item.text }}
            </h3>
        </li>
    </ol>
</template>
