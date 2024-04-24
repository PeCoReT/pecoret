<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '@/components/elements/forms/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/elements/forms/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'HostCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                ip: null,
                dns: null,
                operating_system: null,
                environment: 'Unknown',
                accessible: 'Unknown',
                technologies: []
            },
            assetService: new AssetService()
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
            this.assetService.createHost(this.$api, this.projectId, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'Host created!'
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
    <Button icon="fa fa-plus" label="Host" outlined @click="open"></Button>

    <Dialog header="Create Host" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="ip">IP</label>
                <InputText id="ip" type="text" v-model="model.ip"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="dns">DNS</label>
                <InputText id="dns" type="text" v-model="model.dns"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="os">Operating System</label>
                <InputText id="os" type="text" v-model="model.operating_system"></InputText>
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
