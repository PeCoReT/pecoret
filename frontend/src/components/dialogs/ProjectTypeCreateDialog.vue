<script>
import AdminService from '@/service/AdminService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ProjectTypeCreateDialog',
    components: { MarkdownEditor },
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            model: {
                name: null,
                description: null
            },
            loading: false,
            service: new AdminService()
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
            this.loading = true;
            let data = {
                name: this.model.name,
                description: this.model.description
            };
            this.service
                .createProjectType(this.$api, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Project type Created!',
                        life: 3000,
                        detail: 'Project type created successfully!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getGroups() {
            this.service.getGroups(this.$api).then((response) => {
                this.groupChoices = response.data.results;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Project Type" outlined @click="open"></Button>

    <ModalDialog header="Create Project Type" v-model="visible" :loading="loading" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText id="name" v-model="model.name"></InputText>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
