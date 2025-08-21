<script>
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { Button } from '@/components/ui/button';
import Form from '@/components/form/Form.vue';
import Field from '@/components/form/Field.vue';
import { Input } from '@/components/ui/input';
import { MarkdownEditor } from '@/components/editor';
import ChecklistTabMenu from '@/partials/knowledgebase/ChecklistTabMenu.vue';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { PageHeader } from '@/components/typography';

export default {
    name: 'ItemUpdate',
    components: {
        ModelCombobox,
        ChecklistTabMenu,
        MarkdownEditor,
        Input,
        Field,
        Form,
        ContainerLayout,
        Button,
        PageHeader
    },
    data() {
        return {
            itemId: this.$route.params.itemId,
            model: {}
        };
    },
    mounted() {
        this.$api.get(this.$api.e.checkItemDetail, { pk: this.itemId }).then((response) => {
            this.model = response.data;
        });
    },
    methods: {
        patch() {
            let data = {
                description: this.model.description,
                name: this.model.name,
                item_id: this.model.item_id,
                category: this.model.category
            };
            this.$api.patch(this.$api.e.checkItemDetail, { pk: this.itemId }, data).then(() => {
                this.$router.push({
                    name: 'ChecklistItemList'
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
        <template #right-header>
            <Button variant="destructive"><i class="fa fa-trash"></i> Delete</Button>
        </template>
        <PageHeader>Update Item</PageHeader>
        <Form>
            <Field label="Item ID">
                <Input id="id" v-model="model.item_id" type="text"></Input>
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
            <Button class="w-full" @click="patch">Save</Button>
        </Form>
    </ContainerLayout>
</template>
