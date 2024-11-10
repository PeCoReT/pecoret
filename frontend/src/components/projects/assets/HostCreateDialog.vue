<script>
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'HostCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            projectId: this.$route.params.projectId,
            loading: false,
            model: {
                ip: null,
                dns: null,
                operating_system: null,
                environment: 'Unknown',
                accessible: 'Unknown',
                technologies: []
            },
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.$api.post(this.$api.e.pHostList, { projectPk: this.projectId }, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'Host created!'
                });
                this.$emit('object-created', response.data);
                this.showDialog = false;
            });
        }
    },
    components: {
        TechnologyMultiSelectField,
        AssetEnvironmentSelectField,
        AssetAccessibleSelectField,
        MarkdownEditor
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Host" outlined @click="open"></Button>

    <ModalDialog :loading="loading" header="Create Host" :model-value="showDialog" @onSave="create">
        <Form>
            <Field label="IP">
                <InputText id="ip" type="text" v-model="model.ip"></InputText>
            </Field>
            <InlineFieldGroup>
                <InlineField label="DNS">
                    <InputText id="dns" type="text" v-model="model.dns"></InputText>
                </InlineField>
                <InlineField label="Operating System">
                    <InputText id="os" type="text" v-model="model.operating_system"></InputText>
                </InlineField>
            </InlineFieldGroup>
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
