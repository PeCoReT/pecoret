<script>
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import ProgramSelectField from '@/components/forms/fields/ProgramSelectField.vue';
import {DataTypeChoices, InScopeChoices} from "@/utils/constants";

export default {
    name: 'TargetCreateDialog',
    components: { ProgramSelectField,  MarkdownEditor, ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                data: null,
                scope: 'Undefined',
                program: null,
                description: null
            },
            loading: false,
            technologies: []
        };
    },
    methods: {
        InScopeChoices() {
            return InScopeChoices
        },
        DataTypeChoices() {
            return DataTypeChoices
        },
        open() {
            this.showDialog = true;
        },
        create() {
            this.$api.post(this.$api.e.asTargetList, null, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Target created!',
                    life: 3000,
                    detail: 'Target created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Target" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Target" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Data">
                <InputText v-model="model.data" id="data"></InputText>
            </Field>
            <Field label="Data Type">
                <Select :options="DataTypeChoices()" optionLabel="name" optionValue="value" v-model="model.data_type"></Select>
            </Field>
            <Field label="Program">
                <ProgramSelectField v-model="model.program"></ProgramSelectField>
            </Field>
            <Field label="Scope">
                <Select :options="InScopeChoices()" optionLabel="name" optionValue="value" v-model="model.scope"></Select>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description" id="description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
