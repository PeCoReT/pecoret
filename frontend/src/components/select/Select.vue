<script>
import { Select as SelectUI, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from '@/components/ui/select';

export default {
    name: 'Select',
    emits: ['update:modelValue'],
    components: { SelectUI, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue },
    props: {
        modelValue: {
            required: false
        },
        options: {
            required: true
        },
        placeholder: {
            default: ''
        }
    },
    methods: {
        onUpdateModelValue(value) {
            this.$emit('update:modelValue', value);
        }
    },
    data() {
        return {
            value: this.modelValue || ''
        };
    },
    watch: {
        modelValue: {
            immediate: true,
            handler(value) {
                this.value = value;
            }
        }
    }
};
</script>

<template>
    <SelectUI v-model="value" @update:modelValue="onUpdateModelValue">
        <SelectTrigger>
            <SelectValue class="pr-3" :placeholder="placeholder"></SelectValue>
        </SelectTrigger>
        <SelectContent>
            <SelectGroup>
                <SelectItem v-for="option in options" :value="option.value">{{ option.label }}</SelectItem>
            </SelectGroup>
        </SelectContent>
    </SelectUI>
</template>
