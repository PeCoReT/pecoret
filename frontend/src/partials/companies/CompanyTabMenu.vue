<script>
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default {
    name: 'CompanyTabMenu',
    components: { Tabs, TabsList, TabsTrigger },
    methods: {
        getActiveMenu() {
            for (let i = 0; i < this.items.length; i++) {
                if (this.items[i].route === this.$route.href) {
                    return this.items[i].route;
                }
            }
        }
    },
    data() {
        return {
            items: [
                {
                    label: 'Details',
                    route: this.$router.resolve({
                        name: 'CompanyDetail',
                        params: {
                            companyId: this.$route.params.companyId
                        }
                    }).href
                },
                {
                    label: 'Contacts',
                    route: this.$router.resolve({
                        name: 'CompanyContactList',
                        params: {
                            companyId: this.$route.params.companyId
                        }
                    }).href
                }
            ]
        };
    }
};
</script>

<template>
    <Tabs :default-value="getActiveMenu()" class="w-[400px]">
        <TabsList class="grid w-full grid-cols-2">
            <TabsTrigger v-for="item in items" :key="item.label" :href="item.route" :value="item.route" as="a" class="text-base">
                {{ item.label }}
            </TabsTrigger>
        </TabsList>
    </Tabs>
</template>
