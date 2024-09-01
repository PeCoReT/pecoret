<script>
import ASMonitorService from '@/service/ASMonitorService';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';

export default {
    name: 'ScanFindingDetail',
    components: { TechnologyMultiSelectField },
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
    <BaseLayout :breadcrumbs="breadcrumbs">
        <template #pre-content-right>
            <div class="flex justify-end">
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </template>
        <div class="col-span-12 card">
            <Form>
                <Field label="URL">
                    <InputText v-model="item.url" @update:model-value="patchData({ url: item.url })"></InputText>
                </Field>
                <Field label="Technologies">
                    <TechnologyMultiSelectField v-model="item.technologies" @update:model-value="patchData({ technologies: item.technologies })"></TechnologyMultiSelectField>
                </Field>
            </Form>
        </div>
    </BaseLayout>
</template>
