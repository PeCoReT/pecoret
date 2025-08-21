<script>
import { ToggleGroup as ToggleGroupUI, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Button } from '@/components/ui/button';

export default {
    name: 'ToggleGroup',
    components: { ToggleGroupUI, ToggleGroupItem, Button },
    emits: ['update:modelValue'],
    props: {
        modelValue: {
            required: true
        },
        options: {
            required: true
        }
    },
    methods: {
        updateModelValue(value) {
            this.$emit('update:modelValue', value);
        }
    },
    data() {
        return {
            value: this.modelValue
        };
    },
    watch: {
        modelValue: {
            immediate: true,
            deep: true,
            handler(value) {
                this.value = value;
            }
        }
    }
};
</script>

<template>
    <ToggleGroupUI v-model="value" class="gap-0 rounded bg-background" type="single" @update:modelValue="updateModelValue">
        <ToggleGroupItem v-for="option in options" :key="option.value" :value="option.value" class="w-full flex items-stretch p-0" >
            <Button class="w-full rounded-none m-0" variant="outline" :class="{ 'bg-muted ring-1': option.value === value }">{{ option.label }}</Button>
        </ToggleGroupItem>
    </ToggleGroupUI>
</template>
