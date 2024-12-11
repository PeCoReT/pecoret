<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import AssetTypeSelectField from '@/components/forms/fields/AssetTypeSelectField.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';
import GenericCustomField from '@/components/common/GenericCustomField.vue';
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';

export default {
    name: 'AssetCreate',
    data() {
        return {
            loading: false,
            projectId: this.$route.params.projectId,
            customFields: [],
            breadcrumbs: [
                {
                    label: 'Assets',
                    to: this.$router.resolve({
                        name: 'AssetList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Create',
                    disabled: true
                }
            ],
            model: {
                name: null,
                environment: 'Unknown',
                accessible: 'Unknown',
                asset_type: null,
                description: '',
                technologies: []
            }
        };
    },
    methods: {
        loadAssetTypes() {
            if (!this.model.asset_type) {
                this.customFields = [];
                return;
            }
            this.$api.get(this.$api.e.pAssetCustomFieldList, { pPk: this.projectId }, { asset_type: this.model.asset_type }).then((response) => {
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
                    this.$router.push({
                        name: 'AssetDetail',
                        params: {
                            projectId: this.projectId,
                            assetId: response.data.pk
                        }
                    })
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {
        AssetAccessibleSelectField,
        MarkdownEditor,
        AssetEnvironmentSelectField,
        GenericCustomField,
        TechnologyMultiSelectField,
        AssetTypeSelectField,
        BaseLayout
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <div class="col-span-12 card">
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
                <Field v-for="customField in customFields" :label="customField.label">
                    <GenericCustomField v-model="model['custom_' + customField.name]" :custom-field="customField"></GenericCustomField>
                </Field>
                <Button @click="save" label="Save" class="w-full"></Button>
            </Form>
        </div>
    </BaseLayout>
</template>
