<script>
import AssetService from '@/service/AssetService';
import ServiceUpdateDialog from '@/components/projects/assets/ServiceUpdateDialog.vue';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import markdown from '@/utils/markdown';

export default {
    name: 'ServiceDetail',
    mounted() {
        this.getItem();
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            assetId: this.$route.params.assetId,
            model: { host: {} },
            service: new AssetService(),
            breadcrumbs: [
                {
                    label: 'Services',
                    to: this.$router.resolve({
                        name: 'ServiceList',
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
        getItem() {
            this.service.getService(this.$api, this.projectId, this.assetId).then((response) => {
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
            this.service.deleteService(this.$api, this.projectId, this.assetId).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Confirmed', detail: 'Asset deleted!', life: 3000 });
                this.$router.push({ name: 'ServiceList', params: { projectId: this.projectId } });
            });
        },
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this asset and everyhting related to it?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteAsset();
                }
            });
        }
    },
    components: { DetailCardWithIcon, ServiceUpdateDialog }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <ServiceUpdateDialog @object-updated="getItem" :asset="this.model"></ServiceUpdateDialog>
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="grid">
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Host" icon="fa fa-server" class="surface-ground" :text="model.host.name"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Protocol" icon="fa fa-gears" class="surface-ground" :text="model.protocol"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Product" icon="fa fa-briefcase" class="surface-ground" :text="model.product || '-'"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="State" icon="fa fa-bookmark" class="surface-ground" :text="model.state"></DetailCardWithIcon>
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