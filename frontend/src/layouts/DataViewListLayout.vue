<script>
import { Breadcrumb } from '@/components/breadcrumb';

export default {
    name: 'DataViewListLayout',
    components: { Breadcrumb },
    props: {
        breadcrumbs: {
            required: false
        },
        searchFullWidth: {
            required: false,
            default: false
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

        <div v-if="searchFullWidth === true" class="mt-4 flex justify-start w-full">
            <slot name="search"></slot>
        </div>
        <div v-else>
            <!-- Flex container for search field and create button -->
            <div class="mt-4 flex justify-between items-center w-full">
                <!-- Search field on the left -->
                <div class="flex-1 pr-2">
                    <slot name="search"></slot>
                </div>
                <!-- Create button on the right -->
                <div class="flex-shrink-0">
                    <slot name="create-button"></slot>
                </div>
            </div>
        </div>

        <!-- Main content -->
        <slot name="default"></slot>
    </div>
</template>
