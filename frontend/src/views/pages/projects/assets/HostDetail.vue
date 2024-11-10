<script>
import HostUpdateDialog from '@/components/projects/assets/HostUpdateDialog.vue';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import markdown from '@/utils/markdown';
import ServiceList from '@/components/projects/assets/ServiceList.vue';

export default {
    name: 'HostDetail',
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
                    label: 'Hosts',
                    to: this.$router.resolve({
                        name: 'HostList',
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
            this.$api.get(this.$api.e.pHostDetail, { projectPk: this.projectId, id: this.assetId }).then((response) => {
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
            this.$api.delete(this.$api.e.pHostDetail, { projectPk: this.projectId, pk: this.assetId }).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Confirmed', detail: 'Asset deleted!', life: 3000 });
                this.$router.push({ name: 'HostList', params: { projectId: this.projectId } });
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
    components: { ServiceList, DetailCardWithIcon, HostUpdateDialog }
};
</script>

<template>
    <div class="grid grid-cols-1 mt-3">
        <div class="col-span-1">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-2">
        <div class="col-span-1"></div>
        <div class="col--span-1">
            <div class="flex justify-end">
                <HostUpdateDialog @object-updated="getItem" :asset="this.model"></HostUpdateDialog>
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-1">
        <div class="col-span-1">
            <div class="card">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="DNS" icon="fa fa-earth-europe" class="bg-surface-950" :text="model.dns || '-'"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Environment" icon="fa fa-thumbtack" class="bg-surface-950" :text="model.environment"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Accessibility" icon="fa fa-plug" class="bg-surface-950" :text="model.accessible"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Operating System" icon="fa fa-laptop-code" class="bg-surface-950" :text="model.operating_system || '-'"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid grid-cols-1 mt-3">
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
    <ServiceList :host-id="assetId" :project-id="projectId"></ServiceList>
</template>
