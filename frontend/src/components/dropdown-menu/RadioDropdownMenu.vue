<script>
import { DropdownMenu, DropdownMenuContent, DropdownMenuLabel, DropdownMenuRadioGroup, DropdownMenuRadioItem, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';

export default {
    name: 'RadioDropdownMenu',
    components: {
        Button,
        DropdownMenuRadioItem,
        DropdownMenuContent,
        DropdownMenuRadioGroup,
        DropdownMenuSeparator,
        DropdownMenuLabel,
        DropdownMenuTrigger,
        DropdownMenu
    },
    emits: ['update:modelValue', 'select'],
    props: {
        modelValue: {
            required: true
        },
        items: {
            required: true
        },
        label: {
            required: true
        },
        showClear: {
            default: true
        }
    },
    methods: {
        updateModelValue() {
            this.$emit('update:modelValue', this.selected);
            this.$emit('select', this.selected);
        }
    },
    data() {
        return {
            selected: this.modelValue
        };
    }
};
</script>

<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="ghost">
                {{ label }}
                <i class="w-4 h-4 mr-2 fa fa-chevron-down"></i>
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" class="bg-card text-inherit w-56">
            <DropdownMenuLabel>{{ label }}</DropdownMenuLabel>
            <DropdownMenuSeparator></DropdownMenuSeparator>
            <DropdownMenuRadioGroup v-model="selected" @update:model-value="updateModelValue">
                <DropdownMenuRadioItem v-if="showClear === true" value="">Clear Filter</DropdownMenuRadioItem>
                <DropdownMenuSeparator v-if="showClear === true"></DropdownMenuSeparator>
                <DropdownMenuRadioItem v-for="item in items" :key="item.value" :value="item.value">{{ item.label }} </DropdownMenuRadioItem>
            </DropdownMenuRadioGroup>
        </DropdownMenuContent>
    </DropdownMenu>
</template>
