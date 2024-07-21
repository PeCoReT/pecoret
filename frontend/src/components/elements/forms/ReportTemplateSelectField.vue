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
            handler(value) {
                if (this.choices.length === 0 && typeof value === 'string') {
                    this.model = value;
                    this.choices = [{"name": value}];
                }
            }
        }
    }
};
</script>
<template>
    <label for="report_template">Report Template</label>
    <Dropdown id="report_template" v-model="model" :options="choices" @focus="onFocus" @change="change" option-label="name" option-value="name" :loading="loading"></Dropdown>
</template>
