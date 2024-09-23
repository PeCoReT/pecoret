<script>
import ASMonitorService from '@/service/ASMonitorService';

export default {
    name: 'PortSelectField',
    props: ['modelValue', 'target'],
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
            service: new ASMonitorService()
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
            this.service
                .getPorts(this.$api, { target: this.target, is_web: true })
                .then((response) => {
                    this.choices = response.data.results;
                    this.loaded = true;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        onFilter(event) {
            let params = {
                search: event.value
            };
            this.service.getPorts(this.$api, params).then((response) => {
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
        },
        target: {
            immediate: true,
            deep: true,
            handler() {
                this.loadData();
            }
        }
    }
};
</script>

<template>
    <Select :disabled="!target" v-model="model" :options="choices" @focus="onFocus" optionLabel="display" optionValue="pk" @change="change" :loading="loading" :filter="true" @filter="onFilter"></Select>
</template>
