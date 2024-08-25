<script>
import CompanyService from '@/service/CompanyService';
import ReportTemplateSelectField from '@/components/forms/fields/ReportTemplateSelectField.vue';
import { useAuthStore } from '@/store/auth';

export default {
    name: 'CompanyUpdateDialog',
    props: {
        company: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.company,
            companyService: new CompanyService(),
            authStore: useAuthStore(),
            loading: false
        };
    },
    methods: {
        open() {
            this.visible = true;
        },
        getFileObject(event) {
            this.model.logo = event.files[0];
        },
        patch() {
            let data = {
                name: this.model.name,
                street: this.model.street,
                city: this.model.city,
                zipcode: this.model.zipcode,
                country: this.model.country
            };
            if (this.authStore.groups.isCustomer === false) {
                data['report_template'] = this.model.report_template;
            }
            this.companyService.patchCompany(this.$api, this.company.pk, data).then(() => {
                if (this.model.logo) {
                    this.companyService.uploadCompanyLogo(this.$api, this.company.pk, this.model.logo).then(() => {});
                }
                this.$emit('object-updated', this.model);
                this.visible = false;
            });
        }
    },
    watch: {
        company: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    components: { ReportTemplateSelectField }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" label="Edit" @click="open" outlined></Button>

    <ModalDialog header="Update Company" v-model="visible" :loading="loading" @onSave="patch">
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
            <Field label="Logo">
                <FileUpload @select="getFileObject" mode="basic" accept="image/*"></FileUpload>
            </Field>
        </Form>
    </ModalDialog>
</template>
