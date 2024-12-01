<script>
import AssetUpdateDialog from '@/components/projects/assets/AssetUpdateDialog.vue';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import markdown from '@/utils/markdown';
import BaseLayout from '@/layout/base/BaseLayout.vue';

export default {
    name: 'AssetDetail',
    mounted() {
        this.getItem();
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            assetId: this.$route.params.assetId,
            model: { asset_type: {} },
            customFields: [],
            breadcrumbs: [
                {
                    label: 'Assets',
                    to: this.$router.resolve({
                        name: 'AssetList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Detail',
                    disabled: true
                }
            ]
        };
    },
    methods: {
        getCustomFields() {
            this.customFields = [];
            Object.keys(this.model).forEach((key) => {
                if (key.startsWith('custom_') === true) {
                    this.customFields.push(this.model[key]);

                }
            });
        },
        getItem() {
            this.$api.get(this.$api.e.pAssetDetail, { pPk: this.projectId, pk: this.assetId }).then((response) => {
                this.model = response.data;
                this.getCustomFields()
            });
        },
        renderMarkdown(text) {
            if (text === null || text === undefined) {
                return '';
            }
            return markdown.renderMarkdown(text);
        },
        deleteAsset() {
            this.$api.delete(this.$api.e.pAssetDetail, { pPk: this.projectId, pk: this.assetId }).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Confirmed', detail: 'Asset deleted!', life: 3000 });
                this.$router.push({ name: 'AssetList', params: { projectId: this.projectId } });
            });
        },
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this asset and everything related to it?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteAsset();
                }
            });
        }
    },
    components: { BaseLayout, DetailCardWithIcon, AssetUpdateDialog }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <template #pre-content-right>
            <div class="flex justify-end">
                <AssetUpdateDialog @object-updated="getItem" :asset="this.model"></AssetUpdateDialog>
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </template>
        <div class="col-span-12">
            <div class="card">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-1 md:col-span-3">
                        <DetailCardWithIcon title="Name" icon="fa fa-earth-europe" class="bg-surface-950" :text="model.name"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-1 md:col-span-3">
                        <DetailCardWithIcon title="Environment" icon="fa fa-thumbtack" class="bg-surface-950" :text="model.environment"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-1 md:col-span-3">
                        <DetailCardWithIcon title="Accessibility" icon="fa fa-plug" class="bg-surface-950" :text="model.accessible"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-1 md:col-span-3">
                        <DetailCardWithIcon title="Asset Type" icon="fa fa-code-branch" class="bg-surface-950" :text="model.asset_type.name"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid mt-3 grid-cols-1">
                    <div class="col-span-1">
                        <div class="card bg-surface-950">
                            <label>Description:</label>
                            <div v-html="renderMarkdown(model.description)" class="mt-3"></div>
                        </div>
                    </div>
                </div>
                <div class="grid mt-3 grid-cols-1" v-if="customFields.length > 0">
                    <div class="col-span-1 bg-surface-950 card">
                        <h2 class="text-2xl font-semibold mb-4">Asset Information</h2>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <!-- Key-Value Pair 1 -->
                            <div class="flex flex-col" v-for="customField in customFields">
                                <span class="text-sm font-bold">{{ customField.field.label }}</span>
                                <span class="text-lg ">{{ customField.value }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>
