<script>
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';

export default {
    name: 'ThickClientCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            projectId: this.$route.params.projectId,
            loading: false,
            model: {
                name: null,
                os: null,
                programming_language: null,
                version: null,
                decompile_allowed: 'Unknown',
                environment: 'Unknown',
                accessible: 'Unknown',
                description: null,
                technologies: []
            },
            decompileChoices: [
                {
                    label: 'Unknown',
                    value: 'Unknown'
                },
                {
                    label: 'Yes',
                    value: 'Yes'
                },
                {
                    label: 'No',
                    value: 'No'
                }
            ],
            osChoices: [
                {
                    label: 'Unknown',
                    value: 'Unknown'
                },
                {
                    label: 'Windows',
                    value: 'Windows'
                },
                {
                    label: 'Linux',
                    value: 'Linux'
                }
            ],
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        save() {
            this.loading = true;
            this.$api
                .post(this.$api.e.pGenericAssetList, { projectPk: this.projectId }, this.model)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Thick Client created!',
                        life: 3000,
                        detail: 'Thick client created successfully!'
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
        InlineFieldGroup,
        TechnologyMultiSelectField,
        ModalDialog,
        AssetEnvironmentSelectField,
        AssetAccessibleSelectField,
        MarkdownEditor
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Thick Client" outlined @click="open"></Button>

    <ModalDialog :loading="loading" header="Create Thick Client" v-model="showDialog" @onSave="save">
        <Form>
            <Field label="Name">
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Operating System">
                    <Select :options="osChoices" option-label="label" option-value="value" v-model="model.os"></Select>
                </InlineField>
                <InlineField label="Version">
                    <InputText id="version" type="text" v-model="model.version"></InputText>
                </InlineField>
            </InlineFieldGroup>
            <InlineFieldGroup>
                <InlineField label="Programming Language">
                    <InputText id="programming_language" type="text" v-model="model.programming_language"></InputText>
                </InlineField>
                <InlineField label="Allowed to decompile?">
                    <Select :options="decompileChoices" option-label="label" option-value="value" v-model="model.allowed_decompile"></Select>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Environment">
                <AssetEnvironmentSelectField v-model="model.environment"></AssetEnvironmentSelectField>
            </Field>
            <Field label="Accessible">
                <AssetAccessibleSelectField v-model="model.accessible"></AssetAccessibleSelectField>
            </Field>
            <Field label="Technologies">
                <TechnologyMultiSelectField v-model="model.technologies"></TechnologyMultiSelectField>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
