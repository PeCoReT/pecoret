<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ProgramUpdateDialog',
    components: { ModalDialog, MarkdownEditor },
    props: {
        program: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            showDialog: false,
            model: this.program,
            loading: false,
        };
    },
    watch: {
        program: {
            deep: true,
            immediate: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                description: this.model.description
            };
            this.$api.patch(this.$api.e.asProgramDetail, {pk: this.program.pk}, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Program updated!',
                    life: 3000,
                    detail: 'Program updated successfully'
                });
                this.$emit('object-updated');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-edit" outlined @click="open" size="small"></Button>

    <ModalDialog v-model:loading="loading" header="Update Program" v-model="showDialog" @onSave="patch">
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
