<script>
import { Tabs as TabsUI, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default {
    name: 'Tabs',
    components: { TabsUI, TabsList, TabsTrigger },
    props: {
        items: {
            required: true
        }
    },
    methods: {
        getActiveMenu() {
            for (let i = 0; i < this.items.length; i++) {
                if (this.items[i].route === this.$route.href) {
                    return this.items[i].route;
                }
            }
        }
    }
};
</script>
<template>
    <TabsUI :default-value="getActiveMenu()" class="w-full rounded">
        <TabsList class="w-full flex space-x-4">
            <TabsTrigger v-for="item in items" :key="item.label" :href="item.route" :value="item.route" as="a" class="px-4 flex-1 !text-base hover:bg-accent hover:text-accent-foreground">
                {{ item.label }}
            </TabsTrigger>
        </TabsList>
    </TabsUI>
</template>
