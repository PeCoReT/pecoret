<script>
import ChecklistService from "@/service/ChecklistService";
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ChecklistItemUpdate',
    props: {
        item: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.command,
            service: new ChecklistService(),
            loading: false
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        patch() {
            let data = {
                description: this.model.description,
                name: this.model.name,
                item_id: this.model.item_id
            };
            this.service.patchItem(this.$api, this.item.pk, data).then(() => {
                this.$emit('object-updated', this.model);
                this.visible = false;
            });
        }
    },
    watch: {
        item: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    components: {MarkdownEditor}
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <ModalDialog header="Update Item" v-model="visible" @onSave="patch" :loading="loading">
        <Form>
            <Field label="Item ID">
                <InputText id="id" type="text" v-model="model.item_id"></InputText>

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