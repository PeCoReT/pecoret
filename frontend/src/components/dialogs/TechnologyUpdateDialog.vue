<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyService from '@/service/TechnologyService';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'TechnologyUpdateDialog',
    components: { TechnologyMultiSelectField, MarkdownEditor, ModalDialog },
    emits: ['object-updated'],
    props: {
        technology: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: this.technology,
            loading: false,
            service: new TechnologyService()
        };
    },
    watch: {
        technology: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                description: this.model.description,
                cpe: this.model.cpe,
                homepage: this.model.homepage,
                source_code_url: this.model.source_code_url,
                vendor: this.model.vendor,
                implicit_technologies: this.model.implicit_technologies
            };
            if (this.model.implicit_technologies.length > 0 && this.model.implicit_technologies[0].pk) {
                delete data.implicit_technologies;
            }
            this.service.patchTechnology(this.$api, this.technology.pk, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Technology updated!',
                    life: 3000,
                    detail: 'Technology updated successfully!'
                });
                this.$emit('object-updated');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-edit" outlined @click="open" size="small"></Button>
    <ModalDialog v-model:loading="loading" header="Update Technology" v-model="showDialog" @onSave="patch">
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
    </ModalDialog>
</template>

<style scoped></style>
