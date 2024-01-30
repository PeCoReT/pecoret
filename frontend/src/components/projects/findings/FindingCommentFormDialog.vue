<script>
import FindingService from '@/service/FindingService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'FindingCommentFormDialog',
    components: { MarkdownEditor },
    props: {
        findingId: {
            required: true
        },
        projectId: {
            required: true
        }
    },
    emits: ['object-created'],

    data() {
        return {
            visible: false,
            model: {
                text: null
            },
            service: new FindingService()
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
            let data = {
                comment: this.model.text
            };
            this.service.createComment(this.$api, this.projectId, this.findingId, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'Comment created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
                this.model.text = null;
            });
        }
    }
};
</script>
<template>
    <Button icon="fa fa-plus" label="Comment" outlined @click="open"></Button>
    <Dialog header="New Comment" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="text">Text</label>
                <MarkdownEditor v-model="model.text" id="text"></MarkdownEditor>
            </div>
        </div>
        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
