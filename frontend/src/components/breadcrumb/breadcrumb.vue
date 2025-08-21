<script>
import { Breadcrumb as BreadcrumbUI, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '@/components/ui/breadcrumb';

export default {
    name: 'Breadcrumb',
    components: { BreadcrumbItem, BreadcrumbList, BreadcrumbSeparator, BreadcrumbUI, BreadcrumbLink, BreadcrumbPage },
    props: {
        modelValue: {
            type: Array,
            required: true
        }
    }
};
</script>

<template>
    <BreadcrumbUI class="p-3 overflow-x-auto border rounded bg-surface-900">
        <BreadcrumbList>
            <template v-for="(item, index) in modelValue" :key="index">
                <BreadcrumbItem>
                    <BreadcrumbLink v-if="!item.disabled && item.route" :href="item.route.href">{{ item.label }} </BreadcrumbLink>
                    <BreadcrumbPage v-else>{{ item.label }}</BreadcrumbPage>
                </BreadcrumbItem>
                <BreadcrumbSeparator v-if="index < modelValue.length - 1" />
            </template>
        </BreadcrumbList>
    </BreadcrumbUI>
</template>
