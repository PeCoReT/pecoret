<script>
import { Tabs } from '@/components/tabs';

export default {
    name: 'ChecklistTabMenu',
    components: { Tabs },
    data() {
        return {
            items: [
                {
                    label: 'Checklists',
                    route: this.$router.resolve({
                        name: 'ChecklistList'
                    }).href
                },
                {
                    label: 'Categories',
                    route: this.$router.resolve({
                        name: 'ChecklistCategoryList'
                    }).href
                },
                {
                    label: 'Items',
                    route: this.$router.resolve({
                        name: 'ChecklistItemList',
                    }).href
                },
            ]
        };
    }
};
</script>

<template>
    <Tabs :items="items"></Tabs>
</template>
