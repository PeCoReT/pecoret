<script>
import { DropdownMenu, DropdownMenuContent, DropdownMenuLabel, DropdownMenuRadioGroup, DropdownMenuRadioItem, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';

export default {
    name: 'SeverityDropdownMenu',
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
        }
    },
    methods: {
        updateModelValue() {
            this.$emit('update:modelValue', this.severity);
            this.$emit('select', this.severity);
        }
    },
    data() {
        return {
            severity: this.modelValue
        };
    }
};
</script>

<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button label="Severity" variant="ghost">Severity <i class="fa fa-chevron-down"></i></Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" class="bg-card text-inherit w-56">
            <DropdownMenuLabel>Severity</DropdownMenuLabel>
            <DropdownMenuSeparator></DropdownMenuSeparator>
            <DropdownMenuRadioGroup v-model="severity" @update:model-value="updateModelValue">
                <DropdownMenuRadioItem value="">Clear Filter</DropdownMenuRadioItem>
                <DropdownMenuSeparator></DropdownMenuSeparator>
                <DropdownMenuRadioItem value="Critical">Critical</DropdownMenuRadioItem>
                <DropdownMenuRadioItem value="High">High</DropdownMenuRadioItem>
                <DropdownMenuRadioItem value="Medium">Medium</DropdownMenuRadioItem>
                <DropdownMenuRadioItem value="Low">Low</DropdownMenuRadioItem>
                <DropdownMenuRadioItem value="Informational">Informational</DropdownMenuRadioItem>
            </DropdownMenuRadioGroup>
        </DropdownMenuContent>
    </DropdownMenu>
</template>
