<script>
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'GenericCustomField',
    components: { MarkdownEditor },
    props: {
        modelValue: {
            required: true
        },
        customField: {
            required: true
        }
    },
    emits: ['update:modelValue'],
    methods: {
        change() {
            this.$emit('update:modelValue', this.model);
        }
    },
    data() {
        return {
            model: this.modelValue
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
    <MarkdownEditor v-if="customField.allow_markdown" v-model="model" @update:modelValue="change"></MarkdownEditor>
    <InputNumber v-else-if="customField.field_type === 'integer'" v-model="model" @update:modelValue="change"></InputNumber>
    <InputText v-else v-model="model" @update:modelValue="change"></InputText>
</template>
