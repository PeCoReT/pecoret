<script>
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import ChecklistTabMenu from '@/partials/knowledgebase/ChecklistTabMenu.vue';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import { MarkdownEditor } from '@/components/editor';
import Field from '@/components/form/Field.vue';
import {PageHeader} from "@/components/typography";

export default {
    name: 'CategoryUpdate',
    components: { Field, MarkdownEditor, MultiModelCombobox, ChecklistTabMenu, ContainerLayout, Input, Button, PageHeader },
    data() {
        return {
            model: {},
            categoryId: this.$route.params.categoryId
        };
    },
    mounted() {
        this.$api.get(this.$api.e.checkCategoryDetail, { pk: this.categoryId }).then((response) => {
            this.model = response.data;
        });
    },
    methods: {
        save() {
            let data = {
                name: this.model.name,
                category_id: this.model.category_id,
                summary: this.model.summary
            };
            this.$api.patch(this.$api.e.checkCategoryDetail, { pk: this.categoryId }, data).then(() => {
                this.$router.push({
                    name: 'ChecklistCategoryList'
                });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <ChecklistTabMenu class="md:max-w-lg mt-4"></ChecklistTabMenu>
        </template>
        <PageHeader>Update Category</PageHeader>
        <Form>
            <Field label="Name">
                <Input v-model="model.name"></Input>
            </Field>
            <Field label="Category ID">
                <Input v-model="model.category_id"></Input>
            </Field>
            <Field label="Summary">
                <MarkdownEditor id="summary" v-model="model.summary"></MarkdownEditor>
            </Field>
            <Button class="w-full" @click="save"></Button>
        </Form>
    </ContainerLayout>
</template>
