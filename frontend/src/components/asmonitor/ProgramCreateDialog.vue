<script>
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import ASMonitorService from '@/service/ASMonitorService';
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
            service: new ASMonitorService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.service.createProgram(this.$api, this.model).then(() => {
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
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText v-model="model.name" id="name"></InputText>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <MarkdownEditor v-model="model.description" id="description"></MarkdownEditor>
            </div>
        </div>
    </ModalDialog>
</template>

<style scoped></style>
