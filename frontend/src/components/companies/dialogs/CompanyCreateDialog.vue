<script>
import CompanyService from '@/service/CompanyService';
import ReportTemplateSelectField from '@/components/elements/forms/ReportTemplateSelectField.vue';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';

export default {
    name: 'CompanyCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            loading: false,
            model: {},
            service: new CompanyService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        save() {
            this.loading = true;
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
                this.showDialog = false;
            }).finally(() => {
                this.loading = false;
            })
        }
    },
    components: { ModalDialog, ReportTemplateSelectField }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Company" @click="open" outlined></Button>

    <ModalDialog v-model:loading="loading" header="Create Company" v-model="showDialog" @onSave="save">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" v-model="model.name"></InputText>
            </div>
            <div class="field col-12 md:col-3">
                <label for="street">Street</label>
                <InputText id="street" type="text" v-model="model.street"></InputText>
            </div>
            <div class="field col-12 md:col-3">
                <label for="city">City</label>
                <InputText id="city" type="text" v-model="model.city"></InputText>
            </div>
            <div class="field col-12 md:col-3">
                <label for="zipcode">Zipcode</label>
                <InputText id="zipcode" type="text" v-model="model.zipcode"></InputText>
            </div>
            <div class="field col-12 md:col-3">
                <label for="country">Country</label>
                <InputText id="country" type="text" v-model="model.country"></InputText>
            </div>
            <div class="field col-12">
                <ReportTemplateSelectField v-model="model.report_template"></ReportTemplateSelectField>
            </div>
        </div>
    </ModalDialog>
</template>
