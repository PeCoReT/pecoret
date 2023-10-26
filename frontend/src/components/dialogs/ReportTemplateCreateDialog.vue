<script>
import AdminService from '@/service/AdminService';

export default {
    name: 'ReportTemplateCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            model: {
                name: null,
                package: null,
                status: null
            },
            statusChoices: [
                { title: 'Active', value: 'Active' },
                { title: 'Draft', value: 'Draft' },
                { title: 'Deactivated', value: 'Deactivated' }
            ],
            service: new AdminService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        create() {
            let data = {
                name: this.model.name,
                status: this.model.status,
                package: this.model.package
            };
            this.service.createReportTemplate(this.$api, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Report template Created!',
                    life: 3000,
                    detail: 'Report template created successfully!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Report Template" outlined @click="open"></Button>

    <Dialog header="Create Report Template" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="name">Name</label>
            <InputText id="name" v-model="model.name"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="package">Package</label>
            <InputText id="package" v-model="model.package"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="status">Status</label>
            <Dropdown v-model="model.status" optionLabel="title" :options="statusChoices" optionValue="value"></Dropdown>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>