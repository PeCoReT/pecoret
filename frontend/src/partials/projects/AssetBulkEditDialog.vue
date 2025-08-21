<script>
import { ModalDialog } from '@/components/dialog';
import { AssetAccessibleSelectField, AssetEnvironmentSelectField } from '@/partials/projects';

export default {
    name: 'AssetBulkEditDialog',
    components: { AssetAccessibleSelectField, AssetEnvironmentSelectField, ModalDialog },
    emits: ['object-updated'],
    props: {
        items: {
            required: true
        }
    },
    data() {
        return {
            visible: false,
            fields: {
                environment: null,
                accessible: null
            },
            loading: false,
            projectId: this.$route.params.projectId
        };
    },
    methods: {
        open() {
            this.visible = true;
        },
        async save() {
            let data = {};
            for (let [key, value] of Object.entries(this.fields)) {
                if (value !== null && value !== undefined) {
                    data[key] = value;
                }
            }
            this.loading = true;
            for (let i = 0; i < this.items.length; i++) {
                await this.$api
                    .patch(
                        this.$api.e.pAssetDetail,
                        {
                            pPk: this.projectId,
                            pk: this.items[i].pk
                        },
                        data
                    )
                    .then(() => {});
            }
            this.loading = false;
            this.fields.environment = null;
            this.$toaster({
                title: 'Assets updated!',
                duration: 3000,
                detail: 'Assets updated successfully!'
            });
            this.$emit('object-updated');
            this.visible = false;
        }
    }
};
</script>

<template>
    <Button v-if="items.length > 0" class="mb-2 ml-2" icon="fa fa-edit" outlined @click="open"></Button>

    <ModalDialog :loading="loading" :model-value="visible" header="Bulk Edit" @onSave="save">
        <Form>
            <Field label="Environment">
                <AssetEnvironmentSelectField v-model="fields.environment"></AssetEnvironmentSelectField>
            </Field>
            <Field label="Accessible">
                <AssetAccessibleSelectField v-model="fields.accessible"></AssetAccessibleSelectField>
            </Field>
        </Form>
    </ModalDialog>
</template>
