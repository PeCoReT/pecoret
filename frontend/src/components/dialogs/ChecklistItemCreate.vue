<script>
import ChecklistService from '@/service/ChecklistService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ChecklistItemCreate',
    components: { MarkdownEditor },
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            model: {
                item_id: null,
                name: null,
                description: null,
                category: this.$route.params.categoryId
            },
            loading: false,
            service: new ChecklistService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        create() {
            this.service.createItem(this.$api, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'Item created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Item" outlined @click="open"></Button>

    <ModalDialog header="Create Item" v-model="visible" :loading="loading" @onSave="create">
        <Form>
            <Field label="Item ID">
                <InputText id="item_id" v-model="model.item_id"></InputText>
            </Field>
            <Field label="Name">
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
