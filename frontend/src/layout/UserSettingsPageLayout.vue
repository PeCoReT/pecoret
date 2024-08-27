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
                    route: this.$router.resolve({
                        name: 'UserProfileSettings'
                    })
                },
                {
                    label: 'Notifications',
                    route: this.$router.resolve({
                        name: 'UserNotificationSettings'
                    })
                }
            ]
        };
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <div class="col-span-12">
            <div class="flex gap-3">
                <Menu :model="menuItems">
                    <template #item="{ item, props }">
                        <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
                            <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                                <span :class="item.icon" />
                                <span class="ml-2">{{ item.label }}</span>
                            </a>
                        </router-link>
                        <a v-else v-ripple :href="item.url" :target="item.target" v-bind="props.action">
                            <span :class="item.icon" />
                            <span class="ml-2">{{ item.label }}</span>
                        </a>
                    </template>
                </Menu>
                <div class="w-full card lg:pl-20 lg:pr-20">
                    <div class="col-span-12">
                        <h2 class="text-xl font-bold">{{ headline }}</h2>
                        <h5 class="text-gray-400 mb-3">{{ subheadline }}</h5>
                        <slot></slot>
                    </div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>
