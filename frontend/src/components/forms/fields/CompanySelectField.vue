<script>

export default {
    name: 'CompanySelectField',
    props: {
        modelValue: {
            required: true
        },
        clear: {
            default: true
        }
    },
    emits: ['update:modelValue'],
    data() {
        return {
            items: [],
            model: null
        };
    },
    methods: {
        onFocus() {
            if (this.items.length === 0) {
                this.getItems();
            }
        },
        getItems(params) {
            this.$api.get(this.$api.e.companyList, null, params).then((response) => {
                this.items = response.data.results;
            });
        },
        filter(event) {
            this.getItems({ search: event.value });
        }
    },
    watch: {
        modelValue: {
            deep: true,
            immediate: true,
            handler(value) {
                if (value && value.pk) {
                    this.model = value.pk;
                    if (this.items.length === 0) {
                        this.items = [value];
                    }
                }
            }
        }
    }
};
</script>

<template>
    <Select @focus="onFocus" option-label="name" option-value="pk" v-model="model" :options="items" :show-clear="clear" @update:model-value="this.$emit('update:modelValue', this.model)" :filter="true" @filter="filter"></Select>
</template>
