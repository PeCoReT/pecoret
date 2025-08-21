<script>
export default {
    name: 'ScanTypeSelectField',
    emits: ['update:modelValue'],
    props: {
        modelValue: {
            required: true
        }
    },
    data() {
        return {
            loading: false,
            items: [],
            choices: []
        };
    },
    watch: {
        modelValue: {
            deep: true,
            immediate: true,
            handler(value) {
                if (value && this.choices.length === 0) {
                    for (let i = 0; i < value.length; i++) {
                        this.items.push(value[i].pk);
                    }
                    this.choices = value;
                }
            }
        }
    },
    methods: {
        onFilter(event) {
            let data = {
                search: event.value
            };
            this.$api.get(this.$api.e.asScanTypeList, null, data).then((response) => {
                this.choices = response.data.results;
            });
        },
        getItems() {
            this.$api.get(this.$api.e.asScanTypeList).then((response) => {
                this.choices = response.data.results;
            });
        },
        change() {
            this.$emit('update:modelValue', this.items);
        }
    }
};
</script>

<template>
    <Select v-model="items" :loading="loading" :options="choices" filter optionLabel="name" @filter="onFilter" @focus="getItems" @update:model-value="change"></Select>
</template>
