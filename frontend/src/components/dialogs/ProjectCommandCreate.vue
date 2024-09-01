<script>
import ProjectCommandService from '@/service/ProjectCommandService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ProjectCommandCreate',
    emits: ['object-created'],
    components: { MarkdownEditor },
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            loading: false,
            model: {
                command: null,
                output: null,
                date_run: null
            },
            service: new ProjectCommandService()
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
            this.service.createCommand(this.$api, this.projectId, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'Command created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Command" outlined @click="open"></Button>

    <ModalDialog header="Create Command" v-model="visible" v-model:loading="loading" @onSave="create">
        <Form>
            <Field label="Command">
                <InputText id="name" type="text" v-model="model.command"></InputText>
            </Field>
            <Field label="Output">
                <MarkdownEditor v-model="model.output"></MarkdownEditor>
            </Field>
            <Field label="Date run?">
                <DatePicker v-model="model.date_run" id="date_expire"></DatePicker>
            </Field>
        </Form>
    </ModalDialog>
</template>