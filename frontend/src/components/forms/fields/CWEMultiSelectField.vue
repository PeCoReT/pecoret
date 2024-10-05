<script>
import VulnerabilityService from "@/service/VulnerabilityService";


export default {
    name: 'CWEMultiSelectField',
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
            choices: [],
            service: new VulnerabilityService()
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
            this.service.getCWEs(this.$api, data).then((response) => {
                this.choices = response.data.results;
            });
        },
        getItems() {
            this.service.getCWEs(this.$api).then((response) => {
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
    <MultiSelect filter @filter="onFilter" v-model="items" :loading="loading" optionLabel="name" optionValue="pk" @focus="getItems" @update:model-value="change" :options="choices"></MultiSelect>
</template>
