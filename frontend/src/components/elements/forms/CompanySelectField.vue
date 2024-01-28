<script>
import CompanyService from '@/service/CompanyService';

export default {
    name: 'CompanySelectField',
    props: ['modelValue'],
    emits: ['update:modelValue'],
    data() {
        return {
            service: new CompanyService(),
            items: [],
            model: this.modelValue.pk
        };
    },
    methods: {
        onFocus() {
            if (this.items.length === 0) {
                this.getItems();
            }
        },
        getItems() {
            this.service.getCompanies().then((response) => {
                this.items = response.data.results;
            });
        }
    },
    watch: {
        modelValue: {
            deep: true,
            immediate: true,
            handler(value) {
                if (this.items.length === 0) {
                    this.items = [value];
                }
                this.model = value.pk;
            }
        }
    }
};
</script>

<template>
    <Dropdown @focus="onFocus" option-label="name" option-value="pk" v-model="model" :options="items" show-clear @update:model-value="this.$emit('update:modelValue', this.model)"></Dropdown>
</template>
