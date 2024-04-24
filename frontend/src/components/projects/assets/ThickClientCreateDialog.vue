<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '@/components/elements/forms/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/elements/forms/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'ThickClientCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            projectId: this.$route.params.projectId,
            loading: false,
            model: {
                name: null,
                os: null,
                programming_language: null,
                version: null,
                decompile_allowed: 'Unknown',
                environment: 'Unknown',
                accessible: 'Unknown',
                description: null,
                technologies: []
            },
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
            ],
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
                .createThickClient(this.$api, this.projectId, this.model)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Thick Client created!',
                        life: 3000,
                        detail: 'Thick client created successfully!'
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
    <Button icon="fa fa-plus" label="Thick Client" outlined @click="open"></Button>

    <ModalDialog :loading="loading" header="Create Thick Client" v-model="showDialog" @onSave="save">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="os">Operating System</label>
                <Dropdown :options="osChoices" option-label="label" option-value="value" v-model="model.os"></Dropdown>
            </div>
            <div class="field col-12 md:col-6">
                <label for="version">Version</label>
                <InputText id="version" type="text" v-model="model.version"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="programming_language">Programming Language</label>
                <InputText id="programming_language" type="text" v-model="model.programming_language"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="decompile">Allowed to decompile?</label>
                <Dropdown :options="decompileChoices" option-label="label" option-value="value" v-model="model.allowed_decompile"></Dropdown>
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
