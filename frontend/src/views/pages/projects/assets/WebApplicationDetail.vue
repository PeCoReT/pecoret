<script>
import WebApplicationUpdateDialog from '@/components/projects/assets/WebApplicationUpdateDialog.vue';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import markdown from '@/utils/markdown';

export default {
    name: 'WebApplicationDetail',
    mounted() {
        this.getItem();
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            assetId: this.$route.params.assetId,
            model: {},
            breadcrumbs: [
                {
                    label: 'Web Applications',
                    to: this.$router.resolve({
                        name: 'WebApplicationList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Web Application Detail',
                    disabled: true
                }
            ]
        };
    },
    methods: {
        getItem() {
            this.$api.get(this.$api.e.pWebAppDetail, { projectPk: this.projectId, pk: this.assetId }).then((response) => {
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
            this.$api.delete(this.$api.e.pWebAppDetail, { projectPk: this.projectId, pk: this.assetId }).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Confirmed', detail: 'Asset deleted!', life: 3000 });
                this.$router.push({ name: 'WebApplicationList', params: { projectId: this.projectId } });
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
    components: { DetailCardWithIcon, WebApplicationUpdateDialog }
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
                <WebApplicationUpdateDialog @object-updated="getItem" :asset="this.model"></WebApplicationUpdateDialog>
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-1">
        <div class="col-span-1">
            <div class="card">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-1 md:col-span-3">
                        <DetailCardWithIcon title="Base URL" icon="fa fa-earth-europe" class="bg-surface-950" :text="model.base_url"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-1 md:col-span-3">
                        <DetailCardWithIcon title="Environment" icon="fa fa-thumbtack" class="bg-surface-950" :text="model.environment"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-1 md:col-span-3">
                        <DetailCardWithIcon title="Accessibility" icon="fa fa-plug" class="bg-surface-950" :text="model.accessible"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-1 md:col-span-3">
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
