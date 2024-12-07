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
            this.showDialog = true;
            this.customFields = this.model.custom_fields;
        },
        loadAssetTypes() {
            if (!this.model.asset_type) {
                this.customFields = [];
                return;
            }
            let oldCustomFields = this.customFields;
            this.customFields = [];
            this.$api.get(this.$api.e.pAssetCustomFieldList, { pPk: this.projectId }, { asset_type: this.model.asset_type }).then((response) => {
                for (let i = 0; i < response.data.results.length; i++) {
                    let exists = null;
                    for(let y=0;y<oldCustomFields.length;y++){
                        let item = oldCustomFields[y]
                        console.log(response.data.results[i]);
                        console.log(item.field)
                        if (item.field.pk === response.data.results[i].pk) {
                            exists = item.value
                            break
                        }
                    }
                    this.customFields.push({
                        field: response.data.results[i],
                        value: exists
                    });
                }
            });
        },
        patch() {
            this.loading = true;
            let data = Object.assign({}, this.model);
            if (this.model.technologies.length > 0 && this.model.technologies[0].pk) {
                delete data.technologies;
            }
            if (this.model.asset_type && this.model.asset_type.pk) {
                delete data.asset_type;
            }
            for (let i = 0; i < this.customFields.length; i++) {
                let key = `custom_${this.customFields[i].field.name}`;
                data[key] = this.customFields[i].value;
            }
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
                <AssetTypeSelectField v-model="model.asset_type" @update:model-value="loadAssetTypes"></AssetTypeSelectField>
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
            <Field v-for="customField in customFields" :label="customField.field.label">
                <GenericCustomField v-model="customField.value" :custom-field="customField"></GenericCustomField>
            </Field>
        </Form>
    </ModalDialog>
</template>
