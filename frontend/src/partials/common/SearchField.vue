<script>
import { Input } from '@/components/ui/input';
import { MagnifyingGlassIcon } from '@radix-icons/vue';

export default {
    name: 'SearchField',
    components: { Input, MagnifyingGlassIcon },
    props: {
        modelValue: {
            required: true,
            default: ""
        },
        placeholder: {
            required: false,
            default: 'Keyword search'
        },
        disabled: {
            default: false
        }
    },
    emits: ['search', 'update:modelValue'],
    data() {
        return {
            searchValue: this.modelValue
        };
    },
    methods: {
        search() {
            if (this.disabled !== true) {
                this.$emit('update:modelValue', this.searchValue)
                this.$emit('search', this.searchValue);
            }
        }
    },
    watch: {
        modelValue: {
            deep: true,
            handler(value) {
                this.searchValue = value;
            }
        }
    }
};
</script>

<template>
    <div class="relative w-full items-center">
        <Input id="search" v-model="searchValue" :placeholder="this.placeholder" class="pr-10" type="text"
            v-on:keyup.enter="search" :disabled="disabled"></Input>
        <span class="absolute end-0 inset-y-0 flex items-center justify-center px-2">
            <MagnifyingGlassIcon class="size-6 text-muted-foreground" @click="search" />
        </span>
    </div>
</template>
