<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '@/components/elements/forms/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/elements/forms/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

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
            service: new AssetService(),
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
            this.service.patchThickClient(this.$api, this.$route.params.projectId, this.asset.pk, data).then(() => {
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

    <Dialog header="Update Thick Client" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="formgrid grid p-fluid">
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

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
