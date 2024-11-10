<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ProgramCreateDialog',
    components: { MarkdownEditor, ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                description: null
            },
            loading: false,
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.$api.post(this.$api.e.asProgramList, null, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Program created!',
                    life: 3000,
                    detail: 'Program created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Program" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Program" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name" id="name"></InputText>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description" id="description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
