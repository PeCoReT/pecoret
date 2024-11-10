<script>
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';

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
            projectId: this.$route.params.projectId
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        patch() {
            this.loading = true;
            let data = {
                name: this.model.name,
                base_url: this.model.base_url,
                environment: this.model.environment,
                accessible: this.model.accessible,
                description: this.model.description,
                technologies: this.model.technologies
            };
            if (this.model.technologies.length > 0 && this.model.technologies[0].pk) {
                delete data.technologies;
            }
            this.$api
                .patch(this.$api.e.pWebAppDetail, { projectPk: this.projectId, pk: this.asset.pk })
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

    <ModalDialog v-model:loading="loading" header="Update Web Application" v-model="showDialog" @onSave="patch">
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
