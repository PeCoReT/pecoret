<script>
import { MarkdownEditor } from '@/components/editor';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import Field from '@/components/form/Field.vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import ChecklistTabMenu from '@/partials/knowledgebase/ChecklistTabMenu.vue';
import { PageHeader } from '@/components/typography';

export default {
    name: 'ChecklistItemCreate',
    components: { ChecklistTabMenu, ContainerLayout, Field, ModelCombobox, Input, MarkdownEditor, Button, PageHeader },
    data() {
        return {
            model: {
                item_id: null,
                name: null,
                description: null,
                category: null
            },
            loading: false
        };
    },
    methods: {
        create() {
            this.$api.post(this.$api.e.checkItemList, null, this.model).then(() => {
                this.$toaster({
                    title: 'Created!',
                    duration: 3000,
                    detail: 'Item created!'
                });
                this.$router.push({
                    name: 'ChecklistCategoryDetail',
                    params: { categoryId: this.model.category }
                });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <ChecklistTabMenu class="md:max-w-lg"></ChecklistTabMenu>
        </template>
        <PageHeader>Create Item</PageHeader>
        <Form>
            <Field label="Item ID">
                <Input id="item_id" v-model="model.item_id"></Input>
            </Field>
            <Field label="Name">
                <Input id="name" v-model="model.name" type="text"></Input>
            </Field>
            <Field label="Category">
                <ModelCombobox v-model="model.category" :api-endpoint="this.$api.e.checkCategoryList" variant="form"></ModelCombobox>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </Field>
            <Button class="w-full" @click="create"> Save</Button>
        </Form>
    </ContainerLayout>
</template>
