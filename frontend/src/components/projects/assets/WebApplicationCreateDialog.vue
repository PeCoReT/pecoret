<script>
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'WebApplicationCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            loading: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                base_url: null,
                environment: 'Unknown',
                accessible: 'Unknown',
                description: '',
                technologies: []
            },
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        save() {
            this.loading = true;
            this.$api.post(this.$api.e.pWebAppList, {projectPk: this.projectId}, this.model)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Web Application created!',
                        life: 3000,
                        detail: 'Web application created successfully!'
                    });
                    this.$emit('object-created', response.data);
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {
        TechnologyMultiSelectField,
        ModalDialog,
        AssetEnvironmentSelectField,
        AssetAccessibleSelectField,
        MarkdownEditor
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Web Application" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" header="Create Web Application" v-model="showDialog" @onSave="save">
        <Form>
            <Field label="Name">
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </Field>
            <Field label="Base URL">
                <InputText id="base_url" type="text" v-model="model.base_url"></InputText>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Environment">
                    <AssetEnvironmentSelectField v-model="model.environment"></AssetEnvironmentSelectField>
                </InlineField>
                <InlineField label="Accessible">
                    <AssetAccessibleSelectField v-model="model.accessible"></AssetAccessibleSelectField>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Technologies">
                <TechnologyMultiSelectField v-model="model.technologies"></TechnologyMultiSelectField>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
