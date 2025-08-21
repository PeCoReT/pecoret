<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';

export default {
    name: 'UserSettingsPageLayout',
    components: { BaseLayout },
    props: {
        headline: {
            required: true
        },
        subheadline: {
            required: true
        }
    },
    methods: {
        getActiveClass(route) {
            if (`#${this.$route.path}` === route) {
                return 'pl-3 border-primary bg-accent rounded border-l-2';
            }
            return '';
        }
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Settings',
                    disabled: true
                }
            ],
            menuItems: [
                {
                    label: 'Account',
                    icon: 'fa fa-user',
                    route: this.$router.resolve({
                        name: 'UserProfileSettings'
                    }).href
                },
                {
                    label: 'API Token',
                    icon: 'fa fa-key',
                    route: this.$router.resolve({
                        name: 'APITokenList'
                    }).href
                },
                {
                    label: 'Webhooks',
                    icon: 'fa fa-plug',
                    route: this.$router.resolve({
                        name: 'WebhookList'
                    }).href
                }
            ]
        };
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <div class="col-span-12 card bg-background gap-3">
            <div class="flex gap-3">
                <div class="w-64 !border-0 md:!min-w-[20rem] border-primary p-4 pt-0">
                    <ul class="space-y-1">
                        <li v-for="item in menuItems" :key="item.label" class="hover:bg-accent hover:text-accent-foreground rounded-lg" :class="getActiveClass(item.route)">
                            <a :href="item.route" class="block p-2">
                                <span :class="item.icon" class="mr-2" />
                                {{ item.label }}</a
                            >
                        </li>
                    </ul>
                </div>
                <div class="grow">
                    <div class="grid grid-cols-12">
                        <div class="col-span-12 md:col-start-3 md:col-span-8">
                            <h2 class="text-xl font-bold">{{ headline }}</h2>
                            <h5 class="text-muted-foreground mb-3">{{ subheadline }}</h5>
                            <div class="mb-3">
                                <hr/>
                            </div>
                            <slot></slot>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>
