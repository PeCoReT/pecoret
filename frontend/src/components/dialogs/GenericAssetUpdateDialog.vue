<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '@/components/elements/forms/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/elements/forms/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'GenericAssetUpdateDialog',
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
        patch() {
            let data = {
                name: this.model.name,
                environment: this.model.environment,
                accessible: this.model.accessible,
                description: this.model.description
            };
            this.service.patchGenericAsset(this.$api, this.$route.params.projectId, this.asset.pk, data).then(() => {
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
    components: { AssetEnvironmentSelectField, AssetAccessibleSelectField, MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined label="Edit"></Button>

    <Dialog header="Update Generic Asset" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
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
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>