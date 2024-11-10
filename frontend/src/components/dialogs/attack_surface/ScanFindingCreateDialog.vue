<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import SeveritySelectField from '@/components/forms/fields/SeveritySelectField.vue';
import TagSelectField from '@/components/forms/fields/TagSelectField.vue';
import ProgramSelectField from '@/components/forms/fields/ProgramSelectField.vue';

export default {
    name: 'ScanFindingCreateDialog',
    components: { ProgramSelectField, TagSelectField, MarkdownEditor, ModalDialog, SeveritySelectField },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                severity: null,
                tool: null,
                program: null,
                affected_component: null,
                tags: null,
                description: null,
                comment: null,
                full_output: null
            },
            targetChoices: null,
            cweChoices: null,
            loading: false,
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            if (this.model.tags === null) {
                this.model.tags = [];
            }
            this.$api.post(this.$api.e.asScanFindingList, null, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Finding created!',
                    life: 3000,
                    detail: 'Finding created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Finding" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Finding" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name" id="name"></InputText>
            </Field>
            <Field label="Severity">
                <SeveritySelectField v-model="model.severity"></SeveritySelectField>
            </Field>
            <Field label="Tool">
                <InputText v-model="model.tool" id="tool"></InputText>
            </Field>
            <Field label="Program">
                <ProgramSelectField v-model="model.program"></ProgramSelectField>
            </Field>
            <Field label="Affected Component">
                <InputText v-model="model.affected_component"></InputText>
            </Field>
            <Field label="Tags">
                <TagSelectField v-model="model.tags"></TagSelectField>
            </Field>
            <Field label="Result">
                <MarkdownEditor v-model="model.result"></MarkdownEditor>
            </Field>
            <Field label="Full Output">
                <MarkdownEditor v-model="model.full_output"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
