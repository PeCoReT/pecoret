<script>
import BlankSlate from '@/components/blankslate/BlankSlate.vue';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { Checkbox } from '@/components/ui/checkbox';

export default {
    name: 'DataViewContent',
    components: { Checkbox, DefaultSkeleton, BlankSlate },
    props: {
        loading: {
            required: true
        },
        items: {
            required: true
        },
        blankSlateText: {
            required: false
        },
        blankSlateIcon: {
            required: false
        },
        blankSlateTitle: {
            required: false
        },
        class: {
            default: ''
        },
        selection: {
            required: false,
            default: {}
        },
        showBulkSelect: {
            default: false
        }
    }
};
</script>

<template>
    <div v-if="loading === false">
        <span v-if="items.length < 1">
            <slot name="blankslate"> <BlankSlate v-if="items.length < 1" :icon="blankSlateIcon" :text="blankSlateText" :title="blankSlateTitle" class="border rounded-t-none rounded-b-lg"></BlankSlate> </slot>
        </span>

        <div v-for="(item, index) in items" :key="item.pk" class="flex items-center space-x-4 p-4 border shadow-sm" :class="[this.class, { 'rounded-b-lg': index === items.length - 1 }]">
            <Checkbox v-if="showBulkSelect === true" v-model:checked="selection[item.pk]"></Checkbox>

            <slot :class="item.class" :index="index" :item="item" name="item"></slot>
        </div>
    </div>
    <div v-else>
        <slot name="skeleton">
            <div class="w-full">
                <DefaultSkeleton></DefaultSkeleton>
            </div>
        </slot>
    </div>
</template>
