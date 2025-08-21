<script>
import { GenericCustomField } from '@/partials/common';
import { MarkdownEditor } from '@/components/editor';
import { Input } from '@/components/ui/input';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Select } from '@/components/select';
import { accessibleChoices, environmentChoices } from '@/utils/constants';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import PageHeader from '@/components/typography/PageHeader.vue';

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
                    route: this.$router.resolve({
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
        accessibleChoices() {
            return accessibleChoices;
        },
        environmentChoices() {
            return environmentChoices;
        },
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
                    this.$toaster({
                        title: 'Asset created!',
                        duration: 3000,
                        description: 'Asset created successfully!'
                    });
                    this.$router.push({
                        name: 'AssetDetail',
                        params: {
                            projectId: this.projectId,
                            assetId: response.data.pk
                        }
                    });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {
        PageHeader,
        ContainerLayout,
        ModelCombobox,
        MultiModelCombobox,
        MarkdownEditor,
        GenericCustomField,
        Input,
        Select,
        Button
    }
};
</script>

<template>
    <ContainerLayout>
        <PageHeader>Create Asset</PageHeader>
        <Form>
            <Field label="Name">
                <Input id="name" v-model="model.name" type="text"></Input>
            </Field>
            <Field label="Asset Type">
                <ModelCombobox v-model="model.asset_type" :api-endpoint="this.$api.e.assetTypeList" label="" variant="form" @update:model-value="loadAssetTypes"></ModelCombobox>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Environment">
                    <Select v-model="model.environment" :options="environmentChoices()"></Select>
                </InlineField>
                <InlineField label="Accessible">
                    <Select v-model="model.accessible" :options="accessibleChoices()"></Select>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Technologies">
                <MultiModelCombobox v-model="model.technologies" :options-url="this.$api.e.technologyList" label-field="name" title="" value-field="pk" variant="form"></MultiModelCombobox>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </Field>
            <Field v-for="customField in customFields" :label="customField.label">
                <GenericCustomField v-model="model['custom_' + customField.name]" :custom-field="customField"></GenericCustomField>
            </Field>
            <Button class="w-full" @click="save">Save</Button>
        </Form>
    </ContainerLayout>
</template>
