<script>
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';
import AssetTypeSelectField from '@/components/forms/fields/AssetTypeSelectField.vue';
import GenericCustomField from "@/components/common/GenericCustomField.vue";

export default {
    name: 'AssetCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            loading: false,
            projectId: this.$route.params.projectId,
            customFields: [],
            model: {
                name: null,
                environment: 'Unknown',
                accessible: 'Unknown',
                description: '',
                technologies: []
            }
        };
    },
    methods: {
        open() {
            this.customFields = [];
            this.showDialog = true;
            this.$api.get(this.$api.e.pAssetCustomFieldList, { pPk: this.projectId }, { limit: 200 }).then((response) => {
                this.customFields = response.data.results;
            });
        },
        save() {
            this.loading = true;
            this.$api
                .post(this.$api.e.pAssetList, { pPk: this.projectId }, this.model)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Asset created!',
                        life: 3000,
                        detail: 'Asset created successfully!'
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
        GenericCustomField,
        AssetTypeSelectField,
        TechnologyMultiSelectField,
        ModalDialog,
        AssetEnvironmentSelectField,
        AssetAccessibleSelectField,
        MarkdownEditor
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Asset" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" header="Create Asset" v-model="showDialog" @onSave="save">
        <Form>
            <Field label="Name">
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </Field>
            <Field label="Asset Type">
                <AssetTypeSelectField v-model="model.asset_type"></AssetTypeSelectField>
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
            <Field v-for="customField in customFields" :label="customField.label">
                <GenericCustomField v-model="model['custom_' + customField.name]" :custom-field="customField"></GenericCustomField>
            </Field>
        </Form>
    </ModalDialog>
</template>
