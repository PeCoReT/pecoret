<script>
export default {
    name: 'AssetEnvironmentSelectField',
    props: ['modelValue'],
    emits: ['update:modelValue'],
    methods: {
        change() {
            this.$emit('update:modelValue', this.model);
        }
    },
    data() {
        return {
            model: this.modelValue,
            environmentChoices: [
                { title: 'Unknown', value: 'Unknown' },
                { title: 'Production', value: 'Production' },
                { title: 'Testing', value: 'Testing' },
                { title: 'Staging', value: 'Staging' },
                { title: 'Development', value: 'Development' }
            ]
        };
    }
};
</script>

<template>
    <Select v-model="this.model" :options="environmentChoices" class="w-full" optionLabel="title" optionValue="value" @change="change"></Select>
</template>
