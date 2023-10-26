<script>
import AdminService from '@/service/AdminService';

export default {
    name: 'ReportTemplateUpdateDialog',
    props: {
        template: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.user,
            service: new AdminService(),
            statusChoices: [
                { title: 'Active', value: 'Active' },
                { title: 'Draft', value: 'Draft' },
                { title: 'Deactivated', value: 'Deactivated' }
            ]
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                package: this.model.package,
                status: this.model.status
            };
            this.service.patchReportTemplate(this.$api, this.template.pk, data).then(() => {
                this.$emit('object-updated', this.model);
                this.visible = false;
            });
        }
    },
    watch: {
        template: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <Dialog header="Update Report Template" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
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
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>