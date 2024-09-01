<script>
import CompanyService from '@/service/CompanyService';
import ReportTemplateSelectField from '@/components/forms/fields/ReportTemplateSelectField.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';

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
            this.service
                .createCompany(this.$api, data)
                .then(() => {
                    this.$emit('object-created', this.model);
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { ModalDialog, ReportTemplateSelectField }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Company" @click="open" outlined></Button>

    <ModalDialog v-model:loading="loading" header="Create Company" v-model="showDialog" @onSave="save">
        <Form>
            <Field label="Name">
                <InputText id="name" v-model="model.name"></InputText>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Street">
                    <InputText id="street" type="text" v-model="model.street"></InputText>
                </InlineField>
                <InlineField label="City">
                    <InputText id="city" type="text" v-model="model.city"></InputText>
                </InlineField>
                <InlineField label="Zipcode">
                    <InputText id="zipcode" type="text" v-model="model.zipcode"></InputText>
                </InlineField>
                <InlineField label="Country">
                    <InputText id="country" type="text" v-model="model.country"></InputText>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Report Template">
                <ReportTemplateSelectField v-model="model.report_template"></ReportTemplateSelectField>
            </Field>
        </Form>
    </ModalDialog>
</template>
