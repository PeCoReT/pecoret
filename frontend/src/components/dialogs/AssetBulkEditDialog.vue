<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import AssetEnvironmentSelectField from '@/components/forms/fields/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '@/components/forms/fields/AssetAccessibleSelectField.vue';

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
            this.$toast.add({
                severity: 'success',
                summary: 'Assets updated!',
                life: 3000,
                detail: 'Assets updated successfully!'
            });
            this.$emit('object-updated');
            this.visible = false;
        }
    }
};
</script>

<template>
    <Button icon="fa fa-edit" outlined class="mb-2 ml-2" @click="open" v-if="items.length > 0"></Button>

    <ModalDialog :loading="loading" header="Bulk Edit" :model-value="visible" @onSave="save">
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
