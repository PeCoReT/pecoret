<script>
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ModelCombobox } from '@/components/combobox';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import {PageHeader} from "@/components/typography";

export default {
    name: 'CompanyCreate',
    components: { ContainerLayout, ModelCombobox, Input, Button, PageHeader },
    data() {
        return {
            loading: false,
            model: {},
        };
    },
    methods: {
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
            this.$api
                .post(this.$api.e.companyList, null, data)
                .then((response) => {
                    this.$router.push({ name: 'CompanyDetail', params: { companyId: response.data.pk } });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <PageHeader>Create Company</PageHeader>
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
            <Button class="w-full" @click="save">Save</Button>
        </Form>
    </ContainerLayout>
</template>
