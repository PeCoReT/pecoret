<script>
export default {
    name: 'AssetSelectField',
    props: {
        modelValue: {
            required: true
        },
        projectPk: {
            required: true
        },
        clear: {
            default: true
        },
        placeholder: {
            default: null,
            required: false
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
            this.$api.get(this.$api.e.pAssetList, { pPk: this.projectPk }, params).then((response) => {
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
    <Select
        v-model="model"
        :filter="true"
        :options="items"
        :placeholder="placeholder"
        :show-clear="clear"
        option-label="name"
        option-value="pk"
        @focus="onFocus"
        @update:model-value="this.$emit('update:modelValue', this.model)"
        @filter="filter"
    ></Select>
</template>
