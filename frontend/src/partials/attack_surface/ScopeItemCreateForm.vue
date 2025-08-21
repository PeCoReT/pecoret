<script>
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { ReloadButton } from '@/components/button';
import Select from '@/components/select/Select.vue';
import { asScopeCategoryChoices } from '@/utils/constants';

export default {
    name: 'ScopeItemCreateForm',
    components: { ReloadButton, Select, Checkbox, Label, Input, Button },
    emits: ['update:modelValue', 'update:display', 'save'],
    props: {
        display: {
            required: true
        },
        scope: {
            required: true
        }
    },
    data() {
        return {
            categoryChoices: asScopeCategoryChoices,
            resultOptions: [
                {
                    label: 'Include',
                    value: 'Include'
                },
                {
                    label: 'Exclude',
                    value: 'Exclude'
                }
            ],
            loading: false,
            model: {
                value: null,
                category: null,
                results_in: null,
                annotation: null,
                is_regex: false
            }
        };
    },
    methods: {
        cancel() {
            this.$emit('update:display', false);
        },
        save() {
            this.loading = true;
            this.model.scope = this.scope;
            this.$api
                .post(this.$api.e.asScopeItemList, null, this.model)
                .then(() => {
                    this.$emit('save');
                    this.model.value = null;
                    this.model.category = null;
                    this.model.annotation = null;
                    this.model.is_regex = false;
                    this.model.results_in = null;
                    this.$emit('update:display', false);
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <Card>
        <div class="flex flex-wrap md:flex-nowrap items-stretch gap-4 mt-3">
            <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                <Label class="text-sm font-medium" for="name">Value</Label>
                <Input id="name" v-model="model.value"></Input>
            </div>

            <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                <Label class="text-sm font-medium" for="description">Is Regex</Label>
                <Checkbox v-model:checked="model.is_regex"></Checkbox>
            </div>
            <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                <Label class="text-sm font-medium" for="name">Annotation</Label>
                <Input id="name" v-model="model.annotation"></Input>
            </div>
            <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                <Label class="text-sm font-medium" for="name">Result</Label>
                <Select :options="resultOptions" v-model="model.results_in"></Select>
            </div>
            <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                <Label class="text-sm font-medium" for="name">Category</Label>
                <Select :options="categoryChoices" v-model="model.category"></Select>
            </div>

            <!-- Save and Cancel Buttons (Right Aligned) -->
            <div class="flex gap-2 ml-auto flex-col md:flex-row items-end mt-4 md:mt-0">
                <Button variant="outline" @click="cancel">Cancel</Button>
                <ReloadButton variant="default" @click="save" :disabled="loading" :loading="loading">Save</ReloadButton>
            </div>
        </div>
    </Card>
</template>
