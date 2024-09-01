<script>
import AssetService from '@/service/AssetService';
import MobileApplicationUpdateDialog from '@/components/projects/assets/MobileApplicationUpdateDialog.vue';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import markdown from '@/utils/markdown';

export default {
    name: 'MobileApplicationDetail',
    mounted() {
        this.getItem();
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            assetId: this.$route.params.assetId,
            model: {},
            service: new AssetService(),
            breadcrumbs: [
                {
                    label: 'Mobile Applications',
                    to: this.$router.resolve({
                        name: 'MobileApplicationList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Mobile Application Detail',
                    disabled: true
                }
            ]
        };
    },
    methods: {
        getItem() {
            this.service.getMobileApplication(this.$api, this.projectId, this.assetId).then((response) => {
                this.model = response.data;
            });
        },
        renderMarkdown(text) {
            if (text === null || text === undefined) {
                return '';
            }
            return markdown.renderMarkdown(text);
        },
        deleteAsset() {
            this.service.deleteMobileApplication(this.$api, this.projectId, this.assetId).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Confirmed', detail: 'Asset deleted!', life: 3000 });
                this.$router.push({ name: 'MobileApplicationList', params: { projectId: this.projectId } });
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
    components: { DetailCardWithIcon, MobileApplicationUpdateDialog }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-2">
        <div class="col-span-1">
            <Skeleton v-if="!model.name"></Skeleton>
            <p v-else class="text-lg">{{ model.name }}</p>
        </div>
        <div class="col-span-1">
            <div class="flex justify-end">
                <MobileApplicationUpdateDialog @object-updated="getItem" :asset="this.model"></MobileApplicationUpdateDialog>
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-1">
        <div class="col-span-1">
            <div class="card">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Operating System" icon="fa fa-laptop-code" class="bg-surface-950" :text="model.os"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Environment" icon="fa fa-thumbtack" class="bg-surface-950" :text="model.environment"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Accessibility" icon="fa fa-plug" class="bg-surface-950" :text="model.accessible"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Version" icon="fa fa-code-branch" class="bg-surface-950" :text="model.version || '-'"></DetailCardWithIcon>
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
            </div>
        </div>
    </div>
</template>