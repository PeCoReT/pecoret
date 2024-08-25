<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyService from '@/service/TechnologyService';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'TechnologyCreateDialog',
    components: { TechnologyMultiSelectField, MarkdownEditor, ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                description: null,
                cpe: null,
                homepage: null,
                source_code_url: null,
                vendor: null,
                implicit_technologies: null
            },
            loading: false,
            service: new TechnologyService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            if (this.model.implicit_technologies === null) {
                this.model.implicit_technologies = [];
            }
            this.service.createTechnology(this.$api, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Technology created!',
                    life: 3000,
                    detail: 'Technology created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Technology" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Technology" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name" id="name"></InputText>
            </Field>
            <InlineFieldGroup>
                <InlineField label="CPE">
                    <InputText v-model="model.cpe" id="cpe"></InputText>
                </InlineField>
                <InlineField label="Homepage">
                    <InputText v-model="model.homepage"></InputText>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Vendor">
                <InputText v-model="model.vendor"></InputText>
            </Field>
            <Field label="Source Code URL">
                <InputText v-model="model.source_code_url"></InputText>
            </Field>
            <Field label="Implicit Technologies">
                <TechnologyMultiSelectField v-model="model.implicit_technologies"></TechnologyMultiSelectField>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description" id="description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>

<style scoped></style>
