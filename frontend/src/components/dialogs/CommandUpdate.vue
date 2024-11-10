<script>
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'CommandUpdate',
    props: {
        command: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.command,
            loading: false,
            projectId: this.$route.params.projectId
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
                command: this.model.command,
                output: this.model.output,
                date_run: this.model.date_run
            };
            this.$api
                .patch(
                    this.$api.e.pCommandDetail,
                    {
                        projectPk: this.projectId,
                        pk: this.command.pk
                    },
                    data
                )
                .then(() => {
                    this.$emit('object-updated', this.model);
                    this.visible = false;
                });
        }
    },
    watch: {
        command: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    components: { MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <ModalDialog header="Update Command" v-model="visible" v-model:loading="loading" @onSave="patch">
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
