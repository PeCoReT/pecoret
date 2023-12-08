<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '../elements/forms/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '../elements/forms/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'GenericAssetCreateDialog',
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
                accessible: 'Unknown'
            },
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
            this.service.createGenericAsset(this.$api, this.projectId, this.model).then((response) => {
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
    components: { AssetEnvironmentSelectField, AssetAccessibleSelectField, MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Generic Asset" outlined @click="open"></Button>

    <Dialog header="Create Generic Asset" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </div>

            <div class="field col-12 md:col-6">
                <AssetEnvironmentSelectField v-model="model.environment"></AssetEnvironmentSelectField>
            </div>
            <div class="field col-12 md:col-6">
                <AssetAccessibleSelectField v-model="model.accessible"></AssetAccessibleSelectField>
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