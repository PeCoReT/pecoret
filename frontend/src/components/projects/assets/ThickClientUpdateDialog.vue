<script>
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';

export default {
    name: 'ThickClientUpdateDialog',
    props: {
        asset: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.asset,
            loading: false,
            projectId: this.$route.params.projectId,
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
            ]
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                version: this.model.version,
                environment: this.model.environment,
                accessible: this.model.accessible,
                description: this.model.description,
                os: this.model.os,
                decompile_allowed: this.model.decompile_allowed,
                programming_language: this.model.programming_language,
                technologies: this.model.technologies
            };
            if (this.model.technologies.length > 0 && this.model.technologies[0].pk) {
                delete data.technologies;
            }
            this.$api
                .patch(
                    this.$api.e.pThickClientDetail,
                    {
                        projectPk: this.projectId,
                        pk: this.asset.pk
                    },
                    data
                )
                .then(() => {
                    this.$emit('object-updated', this.model);
                    this.visible = false;
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
        InlineFieldGroup,
        TechnologyMultiSelectField,
        AssetEnvironmentSelectField,
        AssetAccessibleSelectField,
        MarkdownEditor
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined label="Edit"></Button>

    <ModalDialog header="Update Thick Client" v-model="visible" v-model:loading="loading" @onSave="patch">
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
