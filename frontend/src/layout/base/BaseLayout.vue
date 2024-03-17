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
    <div class="grid mt-3">
        <div class="col-12">
            <slot name="breadcrumb">
                <pBreadcrumb v-model="breadcrumbModel"></pBreadcrumb>
            </slot>
        </div>
    </div>
    <slot name="pre-content">
        <div class="grid">
            <div class="col-6">
                <slot name="pre-content-left"></slot>
            </div>
            <div class="col-6">
                <slot name="pre-content-right"></slot>
            </div>
        </div>
    </slot>

    <div class="grid">
        <slot></slot>
    </div>
</template>
