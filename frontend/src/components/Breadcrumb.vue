<script>
import Breadcrumb from 'primevue/breadcrumb';

export default {
    name: 'pBreadcrumb',
    components: { Breadcrumb },
    props: {
        modelValue: {
            required: true
        }
    }
};
</script>

<template>
    <Breadcrumb :model="modelValue" class="rounded">
        <template #item="{ label, item, props }">
            <router-link v-if="item.to" :to="item.to" v-bind="props.action">
                <span v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
            </router-link>
            <a v-else :href="item.url" :target="item.target" v-bind="props.action">
                <span v-if="item.icon" v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
            </a>
        </template>
    </Breadcrumb>
</template>
