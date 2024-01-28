<script>
import CompanyService from '@/service/CompanyService';
import ReportTemplateSelectField from '../elements/forms/ReportTemplateSelectField.vue';
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
            authStore: useAuthStore()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
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

    <Dialog header="Update Company" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="grid formgrid p-fluid">
            <div class="col-12 field">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </div>
            <div class="col-12 field">
                <label for="street">Street</label>
                <InputText id="street" type="text" v-model="model.street"></InputText>
            </div>
            <div class="col-12 md:col-6 field">
                <label for="city">City</label>
                <InputText id="city" type="text" v-model="model.city"></InputText>
            </div>
            <div class="col-12 md:col-6 field">
                <label for="zipcode">Zipcode</label>
                <InputText id="zipcode" type="text" v-model="model.zipcode"></InputText>
            </div>
            <div class="col-12 field">
                <label for="country">Country</label>
                <InputText id="country" type="text" v-model="model.country"></InputText>
            </div>
            <div class="col-12 field">
                <ReportTemplateSelectField v-model="model.report_template" v-if="authStore.groups.isCustomer === false"></ReportTemplateSelectField>
            </div>
            <div class="col-12 field">
                <FileUpload @select="getFileObject" mode="basic" accept="image/*"></FileUpload>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
