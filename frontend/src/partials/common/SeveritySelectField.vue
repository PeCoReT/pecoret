<script>
import { Select } from '@/components/select';

export default {
    name: 'SeveritySelectField',
    props: ['modelValue'],
    emits: ['update:modelValue'],
    components: { Select },
    methods: {
        change() {
            this.$emit('update:modelValue', this.model);
        }
    },
    data() {
        return {
            model: this.modelValue,
            choices: [
                { label: 'Critical', value: 'Critical' },
                { label: 'High', value: 'High' },
                { label: 'Medium', value: 'Medium' },
                { label: 'Low', value: 'Low' },
                { label: 'Informational', value: 'Informational' }
            ]
        };
    },
    watch: {
        modelValue(val) {
            this.model = val;
        }
    }
};
</script>

<template>
    <Select v-model="this.model" :options="choices" class="w-full" @update:modelValue="change"></Select>
</template>
