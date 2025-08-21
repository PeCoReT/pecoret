<script>
import { Breadcrumb } from '@/components/breadcrumb';

export default {
    name: 'BaseListLayout',
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
    <div v-if="breadcrumbs" class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <Breadcrumb v-model="breadcrumbModel"></Breadcrumb>
        </div>
    </div>

    <div class="grid grid-cols-12 mt-3">
        <slot name="pre-content">
            <div class="col-span-6">
                <slot name="head-left"></slot>
            </div>
            <div class="col-span-6">
                <slot name="head-right">
                    <div class="flex justify-end">
                        <slot name="create-button"></slot>
                    </div>
                </slot>
            </div>
        </slot>
    </div>

    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <slot>
                <Card>
                    <slot name="table"></slot>
                </Card>
            </slot>
        </div>
    </div>
</template>
