<script>
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ChecklistCategoryCreate',
    components: { MarkdownEditor },
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            model: {
                category_id: null,
                name: null,
                summary: null
            },
            loading: false,
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
            this.$api.post(this.$api.e.checkCategoryList, null, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
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
    <Button icon="fa fa-plus" label="Category" outlined @click="open"></Button>

    <ModalDialog header="Create Category" v-model="visible" :loading="loading" @onSave="create">
        <Form>
            <Field label="Category ID">
                <InputText id="category_id" v-model="model.category_id"></InputText>
            </Field>
            <Field label="Name">
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </Field>
            <Field label="Summary">
                <MarkdownEditor v-model="model.summary" id="summary"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
