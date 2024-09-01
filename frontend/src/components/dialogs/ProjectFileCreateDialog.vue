<script>
import ProjectService from '@/service/ProjectService';

export default {
    name: 'ProjectFileCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                file: null,
                name: null
            },
            loading: false,
            service: new ProjectService()
        };
    },
    methods: {
        open() {
            this.visible = true;
        },
        getFileObject(event) {
            this.model.file = event.files[0];
        },
        create() {
            let data = {
                name: this.model.name,
                file: this.model.file
            };
            this.service.createProjectFile(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'File added!',
                    life: 3000,
                    detail: 'New file was added!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="File" outlined @click="open"></Button>

    <ModalDialog header="Create File" v-model="visible" v-model:loading="loading" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText id="name" v-model="model.name"></InputText>
            </Field>
            <Field label="File">
                <FileUpload mode="basic" id="file" @select="this.getFileObject"></FileUpload>
            </Field>
        </Form>
    </ModalDialog>
</template>
