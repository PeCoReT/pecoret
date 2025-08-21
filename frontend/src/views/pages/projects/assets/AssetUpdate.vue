<script>
import { GenericCustomField } from '@/partials/common';
import { Button } from '@/components/ui/button';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Input } from '@/components/ui/input';
import { MarkdownEditor } from '@/components/editor';
import { Select } from '@/components/select';
import MultiModelCombobox from '@/components/combobox/MultiModelCombobox.vue';
import { accessibleChoices, environmentChoices } from '@/utils/constants';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import BackLinkButton from '@/components/button/BackLinkButton.vue';

export default {
    name: 'AssetUpdate',
    components: {
        BackLinkButton,
        ContainerLayout,
        MultiModelCombobox,
        Select,
        MarkdownEditor,
        Input,
        ModelCombobox,
        Button,
        GenericCustomField
    },
    mounted() {
        this.getItem();
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
        getItem() {
            this.$api.get(this.$api.e.pAssetDetail, { pPk: this.projectId, pk: this.assetId }).then((response) => {
                this.model = response.data;
            });
        },
        save() {
            this.loading = true;
            this.$api
                .patch(this.$api.e.pAssetList, { pPk: this.projectId }, this.model)
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
    data() {
        return {
            customFields: [],
            model: {},
            projectId: this.$route.params.projectId,
            assetId: this.$route.params.assetId
        };
    }
};
</script>

<template>
    <ContainerLayout>
        <BackLinkButton text="Back to Asset" :href="this.$router.resolve({ name: 'AssetDetail', params: { projectId: this.projectId, assetId: this.assetId } }).href"></BackLinkButton>

        <h2 class="text-2xl mb-3">Update Asset</h2>
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
