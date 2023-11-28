<script>
export default {
    name: 'pTabMenu',
    props: {
        modelValue: {
            required: true
        }
    },
    mounted() {
        this.activeItem = this.modelValue.findIndex((item) => this.$route.path === this.$router.resolve(item.route).path);
    },
    data() {
        return {
            activeItem: null
        };
    },
    methods: {
        onTabChange(event) {
            this.activeItem = event.index;
        }
    },
    watch: {
        modelValue: {
            deep: true,
            handler(newValue) {
                this.activeItem = newValue.findIndex((item) => this.$route.path === this.$router.resolve(item.route).path);
            }
        }
    }
};
</script>

<template>
    <TabMenu :model="modelValue" v-model:activeIndex="activeItem" @tab-change="onTabChange">
        <template #item="{ label, item, props }">
            <router-link v-if="item.route" v-slot="routerProps" :to="item.route" custom>
                <a :href="routerProps.href" v-bind="props.action" @click="($event) => routerProps.navigate($event)">
                    <span v-bind="props.icon" />
                    <span v-bind="props.label">{{ label }}</span>
                </a>
            </router-link>
        </template>
    </TabMenu>
</template>