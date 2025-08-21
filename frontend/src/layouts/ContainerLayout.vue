<script>
import { Breadcrumb } from '@/components/breadcrumb';

export default {
    name: 'ContainerLayout',
    components: { Breadcrumb },
    props: {
        breadcrumbs: {
            required: false
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
    <div class="container mx-auto py-8">
        <div v-if="breadcrumbs" class="mt-4 w-full">
            <Breadcrumb v-model="breadcrumbModel"></Breadcrumb>
        </div>

        <slot name="pre-content"></slot>

        <div class="mb-3">
            <div class="mt-4 flex justify-between items-center w-full">
                <!-- Search field on the left -->
                <div class="flex-1 pr-2">
                    <slot name="left-header"></slot>
                </div>
                <!-- Create button on the right -->
                <div class="flex-shrink-0 flex items-center">
                    <slot name="right-header"></slot>
                </div>
            </div>
        </div>

        <!-- Main content -->
        <slot name="default"></slot>
    </div>
</template>
