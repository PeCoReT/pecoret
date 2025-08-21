<script>
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { CaretSortIcon, CheckIcon } from '@radix-icons/vue';
import { cn } from '@/lib/utils';
import { PopoverArrow } from 'radix-vue';
import { Button } from '@/components/ui/button';

export default {
    name: 'ModelCombobox',
    emits: ['select', 'update:modelValue', 'open'],
    components: {
        Button,
        PopoverArrow,
        Popover,
        PopoverTrigger,
        PopoverContent,
        Command,
        CommandGroup,
        CommandEmpty,
        CommandInput,
        CommandItem,
        CommandList,
        CaretSortIcon,
        CheckIcon
    },
    props: {
        apiEndpoint: {
            required: true
        },
        disabled: {
            default: false,
            required: false
        },
        align: {
            default: 'end'
        },
        labelField: {
            default: 'name'
        },
        valueField: {
            default: 'pk'
        },
        label: {
            required: false,
            default: ''
        },
        modelValue: {
            required: true
        },
        urlArgs: {
            required: false,
            default: null
        },
        variant: {
            required: false,
            default: 'menu'
        },
        fluid: {
            required: false,
            default: false
        },
        triggerFluid: {
            required: false,
            default: false
        },
        queryParams: {
            required: false,
            default: null
        }
    },
    methods: {
        cn,
        getItems(params) {
            if (!params) {
                params = {};
            }
            params['limit'] = 8;
            if (this.queryParams) {
                params = { ...params, ...this.queryParams };
            }
            this.$api.get(this.apiEndpoint, this.urlArgs, params).then((response) => {
                this.items = response.data.results;
            });
        },
        onSearch(query) {
            this.getItems({ search: query });
        },
        onOpen(event) {
            this.$emit('open');
            if (event === true) {
                this.getItems();
            }
        },
        onSelect(ev) {
            let obj = ev.detail.value;
            if (ev.detail) {
                if (this.value === ev.detail.value[this.valueField]) {
                    this.value = '';
                    obj = {};
                } else {
                    this.value = ev.detail.value[this.valueField];
                    this.selectedLabel = ev.detail.value[this.labelField];
                }
            }
            this.open = false;
            this.$emit('update:modelValue', this.value);
            this.$emit('select', obj);
        }
    },
    data() {
        return {
            open: false,
            value: this.modelValue,
            searchTerm: '',
            items: [],
            selectedLabel: null
        };
    },
    watch: {
        modelValue: {
            immediate: true,
            deep: true,
            handler(value) {
                if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
                    // we got a foreign key object
                    this.items = [value];
                    this.value = value[this.valueField];
                    this.selectedLabel = value[this.labelField];
                } else {
                    if (value && this.items.length < 1) {
                        this.$api.get(this.apiEndpoint).then((response) => {
                            this.items = response.data.results;
                            for (let i = 0; i < this.items.length; i++) {
                                if (this.items[i][this.valueField] === value) {
                                    this.value = this.items[i][this.valueField];
                                    this.selectedLabel = this.items[i][this.labelField];
                                    break;
                                }
                            }
                        });
                    }
                }
            }
        }
    }
};
</script>

<template>
    <Popover v-model:open="open" @update:open="onOpen">
        <PopoverTrigger as-child>
            <slot :label="selectedLabel" name="trigger">
                <Button v-if="variant === 'menu'" variant="ghost">
                    {{ label }}
                    <i class="w-4 h-4 mr-2 fa fa-chevron-down"></i>
                </Button>
                <Button v-else :disabled="disabled" class="justify-between" :class="{ 'w-full': triggerFluid === true }" role="combobox" variant="outline">
                    <div class="flex justify-start">
                        <span v-if="selectedLabel">{{ selectedLabel }}</span>
                        <span v-else-if="!selectedLabel && label">{{ label }}</span>
                    </div>
                    <div class="flex justify-end">
                        <i class="ml-2 h-4 w-4 shrink-0 opacity-50 fa fa-chevron-down" />
                    </div>
                </Button>
            </slot>
        </PopoverTrigger>
        <PopoverContent :align="align" class="p-0" :class="fluid === false ? 'PopoverContent' : ''">
            <Command v-model:search-term="searchTerm" @update:search-term="onSearch">
                <CommandInput class="h-9" placeholder="Search ..." />
                <CommandEmpty>No results.</CommandEmpty>
                <CommandList>
                    <CommandGroup>
                        <CommandItem v-for="item in items" :key="item.pk" :value="item" @select="onSelect">
                            {{ item[this.labelField] }}
                            <CheckIcon :class="cn('ml-auto h-4 w-4', value === item[this.valueField] ? 'opacity-100' : 'opacity-0')" />
                        </CommandItem>
                    </CommandGroup>
                </CommandList>
            </Command>
        </PopoverContent>
    </Popover>
</template>

<style>
.PopoverContent {
    min-width: var(--radix-popover-trigger-width);
    max-height: var(--radix-popover-content-available-height);
}
</style>
