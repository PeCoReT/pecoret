<script>
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import AssetTypeSelectField from '@/components/forms/fields/AssetTypeSelectField.vue';
import GenericCustomField from '@/components/common/GenericCustomField.vue';

export default {
    name: 'WebApplicationUpdateDialog',
    props: {
        asset: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            showDialog: false,
            model: this.asset,
            loading: false,
            customFields: [],
            projectId: this.$route.params.projectId
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
        patch() {
            this.loading = true;
            let data = Object.assign({}, this.model);
            if (this.model.technologies.length > 0 && this.model.technologies[0].pk) {
                delete data.technologies;
            }
            if (this.model.asset_type && this.model.asset_type.pk) {
                delete data.asset_type
            }
            Object.keys(this.model).forEach((key) => {
                if (key.startsWith('custom_') === true) {
                    data[key] = this.model[key].value;
                }
            })
            this.$api
                .patch(this.$api.e.pAssetDetail, { pPk: this.projectId, pk: this.asset.pk }, data)
                .then(() => {
                    this.$emit('object-updated', this.model);
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    watch: {
        asset: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    components: {
        GenericCustomField,
        AssetTypeSelectField,
        ModalDialog,
        TechnologyMultiSelectField,
        AssetEnvironmentSelectField,
        AssetAccessibleSelectField,
        MarkdownEditor
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined label="Edit"></Button>

    <ModalDialog v-model:loading="loading" header="Update Asset" v-model="showDialog" @onSave="patch">
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
                <GenericCustomField v-model="model['custom_' + customField.name].value" :custom-field="customField"></GenericCustomField>
            </Field>
        </Form>
    </ModalDialog>
</template>
