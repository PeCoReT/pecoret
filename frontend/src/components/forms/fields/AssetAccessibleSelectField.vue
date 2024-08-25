<script>
export default {
    name: 'AssetAccessibleSelectField',
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
            choices: [
                { title: 'Unknown', value: 'Unknown' },
                { title: 'Accessible', value: 'Accessible' },
                { title: 'Not Accessible', value: 'Not Accessible' }
            ]
        };
    }
};
</script>

<template>
    <Select @change="change" v-model="this.model" :options="choices" optionLabel="title" optionValue="value" class="w-full" id="accessible"></Select>
</template>
