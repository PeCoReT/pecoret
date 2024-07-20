<script>
export default {
    name: 'ReportTemplateSelectField',
    props: ['modelValue'],
    emits: ['update:modelValue'],
    methods: {
        change() {
            this.$emit('update:modelValue', this.model);
        },
        onFocus() {
            if (this.loaded === false) {
                this.loadData();
            }
        },
        loadData() {
            this.loading = true;
            let url = '/report-templates/';
            this.$api
                .get(url)
                .then((response) => {
                    this.choices = response.data.results;
                    this.loaded = true;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    data() {
        let model = this.modelValue;
        return {
            model: model,
            choices: [],
            loading: false,
            loaded: false
        };
    },
    watch: {
        modelValue: {
            immediate: true,
            deep: true,
            handler(value) {
                if (this.choices.length === 0) {
                    if (value) {
                        this.choices = [value];
                    }
                }
            }
        }
    }
};
</script>
<template>
    <label for="report_template">Report Template</label>
    <Dropdown id="report_template" v-model="model" :options="choices" @focus="onFocus" optionLabel="name" optionValue="name" @change="change" :loading="loading"></Dropdown>
</template>
