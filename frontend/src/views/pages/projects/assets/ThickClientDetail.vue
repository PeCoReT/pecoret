<script>
import AssetService from '@/service/AssetService';
import ThickClientUpdateDialog from '@/components/projects/assets/ThickClientUpdateDialog.vue';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import markdown from '@/utils/markdown';

export default {
    name: 'ThickClientDetail',
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
                    label: 'Thick Clients',
                    to: this.$router.resolve({
                        name: 'ThickClientList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Thick Client Detail',
                    disabled: true
                }
            ]
        };
    },
    methods: {
        getItem() {
            this.service.getThickClient(this.$api, this.projectId, this.assetId).then((response) => {
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
            this.service.deleteThickClient(this.$api, this.projectId, this.assetId).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Confirmed', detail: 'Asset deleted!', life: 3000 });
                this.$router.push({ name: 'ThickClientList', params: { projectId: this.projectId } });
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
    components: { DetailCardWithIcon, ThickClientUpdateDialog }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-6">
            <Skeleton v-if="!model.name"></Skeleton>
            <p v-else class="text-lg">{{ model.name }}</p>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <ThickClientUpdateDialog @object-updated="getItem" :asset="this.model"></ThickClientUpdateDialog>
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="grid">
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Operating System" icon="fa fa-laptop-code" class="surface-ground" :text="model.os"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Environment" icon="fa fa-thumbtack" class="surface-ground" :text="model.environment"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Accessibility" icon="fa fa-plug" class="surface-ground" :text="model.accessible"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Version" icon="fa fa-code-branch" class="surface-ground" :text="model.version || '-'"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid">
                    <div class="col-12">
                        <div class="card surface-ground">
                            <label>Description:</label>
                            <div v-html="renderMarkdown(model.description)" class="mt-3"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
