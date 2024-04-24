<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '@/components/elements/forms/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/elements/forms/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'MobileApplicationCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
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
        close() {
            this.visible = false;
        },
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

    <Dialog header="Create Mobile Application" v-model:visible="visible" modal :style="{ width: '70vw' }">
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
            <div class="field col-12">
                <div class="flex align-items-center">
                    <Checkbox v-model="model.certificate_pinning" inputId="cert_pinning" :binary="true" />
                    <label for="cert_pinning" class="ml-2"> Certificate Pinning?</label>
                </div>
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
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
