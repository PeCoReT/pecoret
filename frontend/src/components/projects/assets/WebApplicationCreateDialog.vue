<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '@/components/elements/forms/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/elements/forms/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'WebApplicationCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            loading: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                base_url: null,
                environment: 'Unknown',
                accessible: 'Unknown',
                description: '',
                technologies: []
            },
            service: new AssetService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        save() {
            this.loading = true;
            this.service
                .createWebApplication(this.$api, this.projectId, this.model)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Web Application created!',
                        life: 3000,
                        detail: 'Web application created successfully!'
                    });
                    this.$emit('object-created', response.data);
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {
        TechnologyMultiSelectField,
        ModalDialog,
        AssetEnvironmentSelectField,
        AssetAccessibleSelectField,
        MarkdownEditor
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Web Application" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" header="Create Web Application" v-model="showDialog" @onSave="save">
        <div class="formgrid grid p-fluid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </div>
            <div class="field col-12">
                <label for="base_url">Base URL</label>
                <InputText id="base_url" type="text" v-model="model.base_url"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <AssetEnvironmentSelectField v-model="model.environment"></AssetEnvironmentSelectField>
            </div>
            <div class="field col-12 md:col-6">
                <AssetAccessibleSelectField v-model="model.accessible"></AssetAccessibleSelectField>
            </div>
            <div class="field col-12">
                <label for="technologies">Technologies</label>
                <TechnologyMultiSelectField v-model="model.technologies"></TechnologyMultiSelectField>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </div>
        </div>
    </ModalDialog>
</template>
