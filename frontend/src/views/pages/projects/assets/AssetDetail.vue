<script>
import renderMarkdown from '@/lib/markdown';
import { DetailCardWithIcon } from '@/components/card';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'AssetDetail',
    mounted() {
        this.getItem();
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            assetId: this.$route.params.assetId,
            model: { asset_type: {}, custom_fields: [] }
        };
    },
    methods: {
        renderMarkdown,
        getItem() {
            this.$api.get(this.$api.e.pAssetDetail, { pPk: this.projectId, pk: this.assetId }).then((response) => {
                this.model = response.data;
            });
        },
        deleteAsset() {
            this.$api.delete(this.$api.e.pAssetDetail, { pPk: this.projectId, pk: this.assetId }).then(() => {
                this.$toaster({ title: 'Confirmed', description: 'Asset deleted!', duration: 3000 });
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
    components: { ContainerLayout, DetailCardWithIcon, Button }
};
</script>

<template>
    <ContainerLayout>
        <template #right-header>
            <div class="flex gap-3">
                <Button :href="this.$router.resolve({ name: 'AssetUpdate', params: { projectId: this.projectId, assetId: this.assetId } }).href" as="a" variant="outline"><i class="fa fa-edit"></i> Edit </Button>
                <Button variant="destructive" @click="confirmDialogDelete"><i class="fa fa-trash" /> Delete</Button>
            </div>
        </template>
        <div class="grid grid-cols-12 gap-3">
            <div class="col-span-1 md:col-span-3">
                <DetailCardWithIcon :text="model.name" class="bg-surface-950" icon="fa fa-earth-europe" title="Name"></DetailCardWithIcon>
            </div>
            <div class="col-span-1 md:col-span-3">
                <DetailCardWithIcon :text="model.environment" class="bg-surface-950" icon="fa fa-thumbtack" title="Environment"></DetailCardWithIcon>
            </div>
            <div class="col-span-1 md:col-span-3">
                <DetailCardWithIcon :text="model.accessible" class="bg-surface-950" icon="fa fa-plug" title="Accessibility"></DetailCardWithIcon>
            </div>
            <div class="col-span-1 md:col-span-3">
                <DetailCardWithIcon :text="model.asset_type.name" class="bg-surface-950" icon="fa fa-code-branch" title="Asset Type"></DetailCardWithIcon>
            </div>
        </div>
        <div class="grid mt-3 grid-cols-1">
            <div class="col-span-1">
                <div class="card bg-surface-950">
                    <label>Description:</label>
                    <div class="mt-3" v-html="renderMarkdown(model.description)"></div>
                </div>
            </div>
        </div>
        <div v-if="model.custom_fields.length > 0" class="grid mt-3 grid-cols-1">
            <div class="col-span-1 bg-surface-950 card">
                <h2 class="text-2xl font-semibold mb-4">Asset Information</h2>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Key-Value Pair 1 -->
                    <div v-for="customField in model.custom_fields" class="flex flex-col">
                        <span class="text-sm font-bold">{{ customField.field.label }}</span>
                        <span class="text-lg">{{ customField.value }}</span>
                    </div>
                </div>
            </div>
        </div>
    </ContainerLayout>
</template>
