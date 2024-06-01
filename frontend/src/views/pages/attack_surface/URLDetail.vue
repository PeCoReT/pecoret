<script>
import ASMonitorService from '@/service/ASMonitorService';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'ScanFindingDetail',
    components: { TechnologyMultiSelectField, },
    data() {
        return {
            item: {},
            service: new ASMonitorService(),
            urlId: this.$route.params.urlId,
            breadcrumbs: [
                {
                    label: 'URLs',
                    to: this.$router.resolve({
                        name: 'AttackSurfaceURLList'
                    })
                },
                {
                    label: 'Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getFinding();
    },
    methods: {
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this url?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteURL(this.$api, this.urlId).then(() => {
                        this.$router.push({
                            name: 'AttackSurfaceURLList'
                        });
                    });
                }
            });
        },
        getFinding() {
            this.service.getURL(this.$api, this.urlId).then((response) => {
                this.item = response.data;
            });
        },
        patchData(data) {
            this.service.patchURL(this.$api, this.urlId, data).then((response) => {
                this.item = response.data;
                this.$toast.add({ severity: 'success', summary: 'Updated', detail: 'URL updated!', life: 3000 });
            });
        }
    }
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
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="grid formgrid p-fluid">
                    <div class="field col-12">
                        <label for="description">URL</label>
                        <InputText v-model="item.url" @update:model-value="patchData({ url: item.url })"></InputText>
                    </div>
                    <div class="field col-12">
                        <label for="technologies">Technologies</label>
                        <TechnologyMultiSelectField v-model="item.technologies" @update:model-value="patchData({ technologies: item.technologies })"></TechnologyMultiSelectField>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
