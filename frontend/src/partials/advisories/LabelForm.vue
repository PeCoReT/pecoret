<script>
import { randomHexColor } from '@/lib/colors';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export default {
    name: 'LabelForm',
    components: { Button, Input, Label },
    emits: ['update:modelValue', 'update:display', 'save'],
    props: {
        isPatch: {
            default: false
        },
        modelValue: {
            required: true
        },
        display: {
            required: true
        }
    },
    data() {
        return {
            label: {
                color: randomHexColor(),
                name: null,
                description: null
            }
        };
    },
    methods: {
        randomHexColor,
        cancel() {
            this.$emit('update:display', true);
        },
        save() {
            this.$emit('update:modelValue', this.label);
            this.$emit('save');
        }
    },
    watch: {
        modelValue: {
            deep: true,
            immediate: true,
            handler(value) {
                this.label = value;
            }
        }
    }
};
</script>

<template>
    <div class="flex flex-wrap md:flex-nowrap items-stretch gap-4 mt-3">
        <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
            <Label class="text-sm font-medium" for="name">Name</Label>
            <Input id="name" v-model="label.name"></Input>
        </div>

        <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
            <Label class="text-sm font-medium" for="description">Description</Label>
            <Input v-model="label.description" maxlength="254"></Input>
        </div>

        <!-- Color Field -->
        <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
            <label class="text-sm font-medium" for="color">Color</label>
            <div class="relative w-full items-center">
                <Input v-model="label.color" class="pl-10"></Input>
                <span
                    class="absolute border-r start-0 inset-y-0 flex items-center justify-center px-2 hover:bg-accent rounded hover:text-accent-foreground"
                    @click="
                        () => {
                            this.label.color = this.randomHexColor();
                            this.$emit('update:modelValue', this.label);
                        }
                    "
                >
                    <i class="fa fa-refresh" />
                </span>
            </div>
        </div>

        <!-- Save and Cancel Buttons (Right Aligned) -->
        <div class="flex gap-2 ml-auto flex-col md:flex-row items-end mt-4 md:mt-0">
            <Button variant="outline" @click="cancel">Cancel</Button>
            <Button variant="default" @click="save">Save</Button>
        </div>
    </div>
</template>
