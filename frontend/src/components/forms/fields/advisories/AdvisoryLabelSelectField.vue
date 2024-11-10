<script>

export default {
    name: 'AdvisoryLabelSelectField',
    props: ['modelValue'],
    emits: ['update:modelValue'],
    mounted() {
        this.loadData();
    },
    methods: {
        change() {
            this.$emit('update:modelValue', this.items);
        },
        loadData() {
            this.$api.get(this.$api.e.aLabelList).then((response) => {
                this.choices = response.data.results;
                this.items = [];
                this.modelValue.forEach((item) => {
                    // prefill with already selected items
                    this.items.push(item.pk);
                });
            });
        }
    },
    data() {
        return {
            items: this.modelValue,
            choices: [],
        };
    }
};
</script>

<template>
    <MultiSelect @change="change" id="labels" v-model="items" :options="choices" optionLabel="name" optionValue="pk"> </MultiSelect>
</template>
