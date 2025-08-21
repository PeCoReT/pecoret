<script>
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';

import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { cn } from '@/lib/utils';
import { CalendarIcon } from '@radix-icons/vue';
import {DateFormatter, getLocalTimeZone, parseDate} from '@internationalized/date';

export default {
    name: 'DatePicker',
    components: { Popover, PopoverContent, PopoverTrigger, Calendar, Button, CalendarIcon },
    emits: ['update:modelValue'],
    props: {
        modelValue: {
            required: true
        },
        returnType: {
            required: false,
            default: 'date'
        }
    },
    data() {
        return {
            value: this.modelValue,
            df : new DateFormatter(navigator.language, getLocalTimeZone())
        };
    },
    methods: {
        cn,
        updateModelValue(value) {
            if (this.returnType === 'date') {
                value = value.toString()
            }
            this.$emit('update:modelValue', value);
        }
    },
    watch: {
        modelValue: {
            handler(value) {
                if (value && typeof value === 'string') {
                    this.value = parseDate(value, getLocalTimeZone());
                } else {
                    this.value = value;
                }
            }
        }
    }
};
</script>

<template>
    <Popover>
        <PopoverTrigger as-child>
            <Button :class="cn('justify-start text-left font-normal', !value && 'text-muted-foreground')" variant="outline">
                <CalendarIcon class="mr-2 h-4 w-4" />
                {{ value ? value : 'Pick a date' }}
            </Button>
        </PopoverTrigger>
        <PopoverContent align="start" class="w-auto p-0">
            <Calendar v-model="value" :prevent-deselect="true" initial-focus @update:modelValue="updateModelValue" />
        </PopoverContent>
    </Popover>
</template>
