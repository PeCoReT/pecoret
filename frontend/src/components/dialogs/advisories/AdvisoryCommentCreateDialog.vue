<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import AdvisoryService from '@/service/AdvisoryService';

export default {
    name: 'AdvisoryCommentCreateDialog',
    components: { ModalDialog, MarkdownEditor },
    props: {
        advisoryId: {
            required: true
        }
    },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                comment: null
            },
            loading: false,
            service: new AdvisoryService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            let data = {
                comment: this.model.comment
            };
            this.service.createComment(this.advisoryId, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Comment created!',
                    life: 3000,
                    detail: 'Comment created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>
<template>
    <Button icon="fa fa-plus" label="Comment" outlined @click="open"></Button>
    <ModalDialog @onSave="create" header="New Comment" v-model="showDialog" v-model:loading="loading">
        <Form>
            <Field label="Text">
                <MarkdownEditor v-model="model.comment"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
