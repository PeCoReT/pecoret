<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'MobileApplicationCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            loading: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                os: null,
                certificate_pinning: null,
                environment: 'Unknown',
                accessible: 'Unknown',
                description: null,
                technologies: []
            },
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
            ],
            service: new AssetService()
        };
    },
    methods: {
        open() {
            this.visible = true;
        },
        create() {
            this.service.createMobileApplication(this.$api, this.projectId, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'Mobile application created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    },
    components: { TechnologyMultiSelectField, AssetEnvironmentSelectField, AssetAccessibleSelectField, MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Mobile Application" outlined @click="open"></Button>

    <ModalDialog header="Create Mobile Application" v-model="visible" v-model:loading="loading" @onSave="create">
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
