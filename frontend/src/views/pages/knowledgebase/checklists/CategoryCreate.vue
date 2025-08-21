<script>
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import Form from '@/components/form/Form.vue';
import Field from '@/components/form/Field.vue';
import { Input } from '@/components/ui/input';
import { MarkdownEditor } from '@/components/editor';
import ChecklistTabMenu from '@/partials/knowledgebase/ChecklistTabMenu.vue';
import {PageHeader} from "@/components/typography";

export default {
    name: 'CategoryCreate',
    components: { ChecklistTabMenu, MarkdownEditor, Input, Field, Form, ContainerLayout, PageHeader },
    data() {
        return {
            model: {}
        };
    },
    methods: {
        create() {
            this.$api.post(this.$api.e.checkCategoryList, null, this.model).then((response) => {
                this.$toaster({
                    title: 'Created!',
                    duration: 3000,
                    detail: 'Category created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <template #pre-content>
            <ChecklistTabMenu class="md:max-w-lg mt-4"></ChecklistTabMenu>
        </template>
        <PageHeader>Create Category</PageHeader>
        <Form>
            <Field label="Category ID">
                <Input id="category_id" v-model="model.category_id"></Input>
            </Field>
            <Field label="Name">
                <Input id="name" v-model="model.name" type="text"></Input>
            </Field>
            <Field label="Summary">
                <MarkdownEditor id="summary" v-model="model.summary"></MarkdownEditor>
            </Field>
        </Form>
    </ContainerLayout>
</template>
