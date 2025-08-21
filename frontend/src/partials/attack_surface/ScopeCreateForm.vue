<script>
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import Select from '@/components/select/Select.vue';

export default {
    name: 'ScopeCreateForm',
    components: { Select, Checkbox, Label, Input, Button },
    emits: ['update:modelValue', 'update:display', 'save'],
    props: {
        display: {
            required: true
        },
        program: {
            required: true
        }
    },
    data() {
        return {
            model: {
                name: null
            }
        };
    },
    methods: {
        cancel() {
            this.$emit('update:display', false);
        },
        save() {
            this.model.program = this.program;
            this.$api.post(this.$api.e.asScopeList, null, this.model).then(() => {
                this.$emit('save');
                this.model.name = null;
                this.$emit('update:display', false);
            });
        }
    }
};
</script>

<template>
    <Card>
        <div class="flex flex-wrap md:flex-nowrap items-stretch gap-4 mt-3">
            <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                <Label class="text-sm font-medium" for="name">Name</Label>
                <Input id="name" v-model="model.name"></Input>
            </div>

            <div class="flex gap-2 ml-auto flex-col md:flex-row items-end mt-4 md:mt-0">
                <Button variant="outline" @click="cancel">Cancel</Button>
                <Button variant="default" @click="save">Save</Button>
            </div>
        </div>
    </Card>
</template>
