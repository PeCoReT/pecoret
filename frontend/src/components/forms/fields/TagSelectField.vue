<script>

export default {
    name: 'TagSelectField',
    emits: ['update:modelValue'],
    props: {
        modelValue: {
            required: true
        },
        display: {
            default: 'comma'
        }
    },
    data() {
        return {
            loading: false,
            tags: [],
            tagChoices: [],
        };
    },
    watch: {
        modelValue: {
            deep: true,
            immediate: true,
            handler(value) {
                if (value && this.tagChoices.length === 0) {
                    for (let i = 0; i < value.length; i++) {
                        this.tags.push(value[i].pk);
                    }
                    this.tagChoices = value;
                }
            }
        }
    },
    methods: {
        onFilter(event) {
            this.$api.get(this.$api.e.asTagList, null, { search: event.value }).then((response) => {
                this.tagChoices = response.data.results;
            });
        },
        getTags() {
            this.$api.get(this.$api.e.asTagList).then((response) => {
                this.tagChoices = response.data.results;
            });
        },
        change() {
            this.$emit('update:modelValue', this.tags);
        }
    }
};
</script>

<template>
    <MultiSelect filter :display="this.display" @filter="onFilter" v-model="tags" :loading="loading" optionLabel="name" optionValue="pk" @focus="getTags" @change="change" :options="tagChoices"></MultiSelect>
</template>
