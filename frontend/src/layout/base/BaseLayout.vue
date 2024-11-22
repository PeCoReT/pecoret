<script>
export default {
    name: 'BaseLayout',
    props: {
        breadcrumbs: {
            required: true
        }
    },
    data() {
        return {
            breadcrumbModel: this.breadcrumbs
        };
    }
};
</script>

<template>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <slot name="breadcrumb">
                <pBreadcrumb v-model="breadcrumbModel"></pBreadcrumb>
            </slot>
        </div>
    </div>
    <slot name="pre-content">
        <div class="grid grid-cols-12 mt-3">
            <div class="col-span-6">
                <slot name="pre-content-left"></slot>
            </div>
            <div class="col-span-6">
                <slot name="pre-content-right"></slot>
            </div>
        </div>
    </slot>

    <div class="grid grid-cols-12 gap-3 mt-3 mb-5">
        <slot></slot>
    </div>
</template>
