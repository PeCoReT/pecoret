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
          if (this.$route.path === route.path) {
              return 'pl-3 border-primary bg-gray-700 rounded border-l-2'
          }
          return ''
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
                    })
                },
                {
                    label: 'Notifications',
                    icon: 'fa fa-envelope',
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
        <div class="col-span-12 card gap-3">
            <div class="flex gap-3">
                <Menu :model="menuItems" class="!border-0 md:!min-w-[20rem]">
                    <template #item="{ item, props }">
                        <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
                            <a :href="href" v-bind="props.action" @click="navigate" :class="getActiveClass(item.route)">
                                <span :class="item.icon" />
                                <span class="ml-2">{{ item.label }}</span>
                            </a>
                        </router-link>
                        <a v-else :href="item.url" :target="item.target" v-bind="props.action">
                            <span :class="item.icon" />
                            <span class="ml-2">{{ item.label }}</span>
                        </a>
                    </template>
                </Menu>
                <div class="grow">
                    <div class="grid grid-cols-12">
                        <div class="col-span-12 md:col-start-4 md:col-span-5">
                            <h2 class="text-xl font-bold">{{ headline }}</h2>
                            <h5 class="text-gray-400 mb-3">{{ subheadline }}</h5>
                            <slot></slot>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>
