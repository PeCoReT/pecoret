<script>
import CompanyService from '@/service/CompanyService';
import ReportTemplateSelectField from '../elements/forms/ReportTemplateSelectField.vue';

export default {
    name: 'CompanyCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            model: {},
            service: new CompanyService()
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
                street: this.model.street,
                city: this.model.city,
                zipcode: this.model.zipcode,
                country: this.model.country,
                report_template: this.model.report_template
            };
            this.service.createCompany(this.$api, data).then(() => {
                this.$emit('object-created', this.model);
                this.visible = false;
            });
        }
    },
    components: { ReportTemplateSelectField }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Company" @click="open" outlined></Button>

    <Dialog header="Create Company" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="name">Name</label>
            <InputText id="name" type="text" v-model="model.name"></InputText>
        </div>

        <div class="flex flex-column gap-2">
            <label for="street">Street</label>
            <InputText id="street" type="text" v-model="model.street"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="city">City</label>
            <InputText id="city" type="text" v-model="model.city"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="zipcode">Zipcode</label>
            <InputText id="zipcode" type="text" v-model="model.zipcode"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="country">Country</label>
            <InputText id="country" type="text" v-model="model.country"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <ReportTemplateSelectField v-model="model.report_template"></ReportTemplateSelectField>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>