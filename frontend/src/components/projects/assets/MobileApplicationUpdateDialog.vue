<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'MobileApplicationUpdateDialog',
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
            service: new AssetService(),
            loading: false,
            osChoices: [
                {
                    label: 'Unknown',
                    value: 'Unknown'
                },
                {
                    label: 'Android',
                    value: 'Android'
                },
                {
                    label: 'iOS',
                    value: 'iOS'
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
                technologies: this.model.technologies
            };
            if (this.model.technologies.length > 0 && this.model.technologies[0].pk) {
                delete data.technologies;
            }
            this.service.patchMobileApplication(this.$api, this.$route.params.projectId, this.asset.pk, data).then(() => {
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
    components: { TechnologyMultiSelectField, AssetEnvironmentSelectField, AssetAccessibleSelectField, MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined label="Edit"></Button>

    <ModalDialog header="Update Mobile Application" v-model="visible" v-model:loading="loading" @onSave="patch">
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
            <Field>
                <div class="flex items-center">
                    <Checkbox v-model="model.certificate_pinning" inputId="cert_pinning" :binary="true" />
                    <label class="ml-2">Certificate Pinning?</label>
                </div>
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
