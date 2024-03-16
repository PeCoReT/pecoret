<script>
export default {
    name: 'BaseListLayout',
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
            <pBreadcrumb v-model="breadcrumbModel"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <slot name="head-left"></slot>
        </div>
        <div class="col-6">
            <slot name="head-right">
                <div class="flex justify-content-end">
                    <slot name="create-button"></slot>
                </div>
            </slot>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <slot>
                <div class="card">
                    <slot name="table"></slot>
                </div>
            </slot>
        </div>
    </div>
</template>
