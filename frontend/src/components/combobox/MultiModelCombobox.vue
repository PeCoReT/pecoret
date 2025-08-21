<script>
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator } from '@/components/ui/command';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Button } from '@/components/ui/button';
import { ref, toRaw } from 'vue';
import { Input } from '@/components/ui/input';

export default {
    name: 'MultiModelCombobox',
    emits: ['update:modelValue'],
    components: {
        Input,
        Button,
        Popover,
        PopoverContent,
        PopoverTrigger,
        CommandSeparator,
        CommandItem,
        CommandGroup,
        CommandEmpty,
        CommandList,
        CommandInput,
        Command
    },

    props: {
        modelValue: {
            required: true
        },
        title: {
            type: String,
            required: true
        },
        options: {
            type: Array,
            default: () => []
        },
        optionsUrl: {
            required: true
        },
        labelField: {
            type: String,
            default: 'name'
        },
        valueField: {
            type: String,
            default: 'pk'
        },
        align: {
            default: 'start'
        },
        disabled: {
            default: false,
            required: false
        },
        variant: {
            default: 'form'
        }
    },

    data() {
        return {
            model: this.modelValue,
            selectedValues: new Set(this.model),
            // filter function only works on "value" field. so this is a workaround!
            optionsList: [],
            q: '',
            selectedLabel: [],
            open: false
        };
    },

    methods: {
        updateOptionList() {
            let params = {
                limit: 7
            };
            if (this.q !== '') {
                params['search'] = this.q;
            }

            this.$api.get(this.optionsUrl, null, params).then((response) => {
                // if there is a selected element, keep it on search
                let selected = [...toRaw(this.model)];
                response.data.results.forEach((result) => {
                    if (!selected.some((item) => item.pk === result.pk)) {
                        selected.push(result);
                    }
                });
                this.optionsList = ref(selected);
            });
        },

        filterFunction() {
            if (this.q !== '') {
                this.updateOptionList();
            }
        },

        toggleSelection(option) {
            if (this.selectedValues.has(option[this.valueField])) {
                // delete option if already selected
                this.selectedValues.delete(option[this.valueField]);
                this.model = this.model.filter((value) => value[this.valueField] !== option[this.valueField]);
            } else {
                this.selectedValues.add(option[this.valueField]);
                this.model.push(option);
            }
            this.$emit('update:modelValue', Array.from(toRaw(this.selectedValues)));
        },

        onOpen(event) {
            if (event === true && this.optionsList.length < 1) {
                this.updateOptionList();
            }
        },

        clearSelections() {
            this.selectedLabel = [];
            this.model = [];
            this.selectedValues.clear();
            this.$emit('update:modelValue', this.model);
        }
    },

    watch: {
        modelValue: {
            immediate: true,
            deep: true,
            handler(value) {
                if (Array.isArray(value) && this.optionsList.length < 1) {
                    this.optionsList = value;
                    this.model = [];
                    this.selectedValues = new Set();
                    for (let i = 0; i < value.length; i++) {
                        this.model.push(this.optionsList[i]);
                        this.selectedValues.add(this.optionsList[i][this.valueField]);
                    }
                }
            }
        }
    }
};
</script>

<template>
    <div class="flex flex-col gap-2">
        <Popover v-model:open="open" @update:open="onOpen">
            <PopoverTrigger as-child>
                <Button :disabled="disabled" class="justify-between" role="combobox" variant="outline" v-if="variant === 'form'">
                    <div class="flex justify-start">
                        <span v-if="selectedValues.size < 1" class="text-muted-foreground">{{ title }}</span>
                        <template v-if="selectedValues.size > 0">
                            <span class="rounded-sm px-1 font-normal lg:hidden"> {{ selectedValues.size }} selected </span>
                            <div class="hidden space-x-1 lg:flex">
                                <span v-if="selectedValues.size > 3" class="rounded-sm px-1 font-normal"> {{ selectedValues.size }} selected </span>
                                <template v-else>
                                    <span v-for="option in optionsList.filter((op) => selectedValues.has(op[valueField]))" :key="option[valueField]">
                                        {{ option[labelField] }}
                                    </span>
                                </template>
                            </div>
                        </template>
                    </div>
                    <div class="flex justify-end">
                        <i class="ml-2 h-4 w-4 shrink-0 opacity-50 fa fa-chevron-down" />
                    </div>
                </Button>
                <Button v-else variant="ghost">
                    {{ title }}
                    <i class="w-4 h-4 mr-2 fa fa-chevron-down"></i>
                </Button>
            </PopoverTrigger>
            <PopoverContent :align="align" class="w-full p-0 PopoverContent">
                <div class="relative w-full items-center">
                    <Input v-model="q" class="bg-muted pl-10" @update:model-value="filterFunction"></Input>
                    <span class="absolute start-0 inset-y-0 flex items-center justify-center px-2">
                        <i class="fa fa-search"></i>
                    </span>
                </div>
                <ul>
                    <li v-for="option in optionsList" :key="option[valueField]" :value="optionsList[valueField]" class="flex p-2 items-center w-full hover:bg-accent hover:text-accent-foreground hover:cursor-pointer" @click="toggleSelection(option)">
                        <div :class="['mr-2 flex h-4 w-4 items-center justify-center rounded-sm border border-primary', selectedValues.has(option[valueField]) ? 'bg-primary text-primary-foreground' : 'opacity-50 [&_svg]:invisible']">
                            <i v-if="selectedValues.has(option[valueField])" class="h-4 w-4 fa fa-check" />
                        </div>
                        <span>{{ option[labelField] }}</span>
                    </li>
                    <li>
                        <Button @click="clearSelections" variant="ghost" class="w-full border-t rounded-t-none">Clear Selection </Button>
                    </li>
                </ul>
            </PopoverContent>
        </Popover>
    </div>
</template>

<style>
.PopoverContent {
    width: var(--radix-popover-trigger-width);
    max-height: var(--radix-popover-content-available-height);
}
</style>
