<script>
import { DropdownMenu, DropdownMenuContent, DropdownMenuLabel, DropdownMenuRadioGroup, DropdownMenuRadioItem, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';

export default {
    name: 'SortListDropdownMenu',
    components: {
        DropdownMenu,
        DropdownMenuLabel,
        DropdownMenuRadioItem,
        DropdownMenuRadioGroup,
        DropdownMenuSeparator,
        DropdownMenuContent,
        DropdownMenuTrigger,
        Button
    },
    emits: ['sort', 'update:modelValue', 'update:field'],
    props: {
        items: {
            required: true
        },
        modelValue: {}
    },
    data() {
        return {
            sortField: null,
            sortDirection: null
        };
    },
    watch: {
        items: {
            deep: true,
            immediate: true,
            handler() {}
        },
        modelValue: {
            immediate: true,
            handler(value) {
                if (value) {
                    this.stringToFields(value)
                }
            }
        }
    },
    methods: {
        stringToFields(value){
            if (value.startsWith('-')) {
                this.sortDirection = "newest"
                this.sortField = value.substring(1)
            } else {
                this.sortDirection = "oldest"
                this.sortField = value;
            }
        },

        updateField() {
            this.$emit('update:modelValue', this.buildOrdering(this.sortField, this.sortDirection));
        },
        buildOrdering(field, direction) {
            if (direction === 'newest') {
                return `-${field}`;
            }
            return field;
        },
        updateDirection() {
            this.$emit('update:modelValue', this.buildOrdering(this.sortField, this.sortDirection));
        }
    }
};
</script>

<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="ghost">
                Sort
                <i class="w-4 h-4 mr-2 fa fa-chevron-down"></i>
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" class="bg-card text-inherit w-56">
            <DropdownMenuLabel>Sort by</DropdownMenuLabel>
            <DropdownMenuSeparator></DropdownMenuSeparator>
            <DropdownMenuRadioGroup v-model="sortField" @update:model-value="updateField">
                <DropdownMenuRadioItem v-for="item in items" :key="item.value" :value="item.value">
                    {{ item.label }}
                </DropdownMenuRadioItem>
            </DropdownMenuRadioGroup>
            <DropdownMenuSeparator></DropdownMenuSeparator>
            <DropdownMenuRadioGroup v-model="sortDirection" @update:model-value="updateDirection">
                <DropdownMenuRadioItem value="oldest">Oldest</DropdownMenuRadioItem>
                <DropdownMenuRadioItem value="newest">Newest</DropdownMenuRadioItem>
            </DropdownMenuRadioGroup>
        </DropdownMenuContent>
    </DropdownMenu>
</template>
