<script>

export default {
    name: 'ProgramSelectField',
    props: ['modelValue'],
    emits: ['update:modelValue', 'change'],
    data() {
        let model = this.modelValue;
        if (this.modelValue && this.modelValue.pk) {
            model = this.modelValue.pk;
        }
        return {
            model: model,
            choices: [],
            loading: false,
            loaded: false,
        };
    },
    methods: {
        change() {
            this.$emit('update:modelValue', this.model);
            for (let i = 0; i < this.choices.length; i++) {
                if (this.choices[i].pk === this.model) {
                    this.$emit('change', this.choices[i]);
                    break;
                }
            }
        },
        onFocus() {
            if (this.loaded === false) {
                this.loadData();
            }
        },
        loadData() {
            this.loading = true;
            this.$api.get(this.$api.e.asProgramList)
                .then((response) => {
                    this.choices = response.data.results;
                    this.loaded = true;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onFilter(event) {
            this.$api.get(this.$api.e.asProgramList, null, {search: event.value}).then((response) => {
                this.choices = response.data.results;
            });
        }
    },
    watch: {
        modelValue: {
            immediate: true,
            deep: true,
            handler(value) {
                if (this.choices.length === 0) {
                    if (value && value.pk) {
                        this.choices = [value];
                    }
                }
            }
        }
    }
};
</script>

<template>
    <Select v-model="model" :options="choices" @focus="onFocus" optionLabel="name" optionValue="pk" @change="change" :loading="loading" :filter="true" @filter="onFilter"></Select>
</template>
