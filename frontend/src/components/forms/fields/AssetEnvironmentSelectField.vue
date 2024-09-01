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
    <Select @change="change" v-model="this.model" :options="environmentChoices" optionLabel="title" optionValue="value" class="w-full"></Select>
</template>
