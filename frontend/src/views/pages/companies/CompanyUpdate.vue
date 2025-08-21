<script>
import { useAuthStore } from '@/store/auth';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ModelCombobox } from '@/components/combobox';
import { Label } from '@/components/ui/label';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import PageHeader from "@/components/typography/PageHeader.vue";
import BackLinkButton from "@/components/button/BackLinkButton.vue";

export default {
    name: 'CompanyUpdate',
    components: {BackLinkButton, PageHeader, ContainerLayout, Label, ModelCombobox, Input, Button },
    data() {
        return {
            model: {},
            authStore: useAuthStore(),
            loading: false,
            companyId: this.$route.params.companyId
        };
    },
    mounted() {
        this.$api.get(this.$api.e.companyDetail, { pk: this.companyId }).then((response) => {
            this.model = response.data;
        });
    },
    methods: {
        getFileObject(event) {
            this.model.logo = event.target.files[0];
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
            this.$api.patch(this.$api.e.companyDetail, { pk: this.companyId }, data).then(() => {
                if (this.model.logo) {
                    let formData = new FormData();
                    formData.append('logo', this.model.logo);
                    this.$api.patch(this.$api.e.companyDetail, { pk: this.companyId }, formData).then(() => {});
                }
                this.$router.push({ name: 'CompanyDetail', params: { companyId: this.companyId } });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <BackLinkButton text="Back to Company" :href="this.$router.resolve({name: 'CompanyDetail', params: {companyId: this.companyId}}).href"></BackLinkButton>
        <PageHeader>Update Company</PageHeader>
        <Form>
            <Field label="Name">
                <Input id="name" v-model="model.name"></Input>
            </Field>
            <InlineFieldGroup>
                <InlineField label="Street">
                    <Input id="street" v-model="model.street" type="text"></Input>
                </InlineField>
                <InlineField label="City">
                    <Input id="city" v-model="model.city" type="text"></Input>
                </InlineField>
                <InlineField label="Zipcode">
                    <Input id="zipcode" v-model="model.zipcode" type="text"></Input>
                </InlineField>
                <InlineField label="Country">
                    <Input id="country" v-model="model.country" type="text"></Input>
                </InlineField>
            </InlineFieldGroup>
            <Field label="Report Template">
                <ModelCombobox v-model="model.report_template" :api-endpoint="this.$api.e.reportTemplateList" align="start" label="Report Template" value-field="name">
                    <template #trigger="{ label }">
                        <Button class="justify-between" role="combobox" variant="outline">
                            {{ model.report_template ? label : 'Select template...' }}
                            <i class="ml-2 h-4 w-4 shrink-0 opacity-50 fa fa-chevron-down" />
                        </Button>
                    </template>
                </ModelCombobox>
            </Field>
            <Field label="Logo">
                <div class="grid w-full items-center">
                    <Input ccept="image/*" class="w-full file:text-foreground" type="file" @change="getFileObject" />
                </div>
            </Field>
            <Button :loading="loading" class="w-full" label="Save" @click="patch"></Button>
        </Form>
    </ContainerLayout>
</template>
