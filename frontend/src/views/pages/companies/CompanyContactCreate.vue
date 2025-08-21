<script>
import BaseLayout from '@/layout/base/BaseLayout.vue';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import PageHeader from '@/components/typography/PageHeader.vue';
import BackLinkButton from '@/components/button/BackLinkButton.vue';

export default {
    name: 'CompanyContactCreate',
    components: { BackLinkButton, PageHeader, ContainerLayout, BaseLayout, Textarea, Input, Button },
    data() {
        return {
            companyId: this.$route.params.companyId,
            loading: false,
            model: {
                first_name: null,
                last_name: null,
                phone: null,
                role: null,
                pgp_public_key: null,
                email: null
            }
        };
    },
    methods: {
        create() {
            let data = {
                first_name: this.model.first_name,
                last_name: this.model.last_name,
                phone: this.model.phone,
                pgp_public_key: this.model.pgp_public_key,
                email: this.model.email,
                role: this.model.role
            };
            this.$api.post(this.$api.e.cContactList, { cPk: this.companyId }, data).then(() => {
                this.$toaster({
                    title: 'Created!',
                    detail: 'Contact created for company!',
                    duration: 3000
                });
                this.$router.push({ name: 'CompanyContactList', params: { companyId: this.companyId } });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout>
        <BackLinkButton text="Back To Contacts" :href="this.$router.resolve({ name: 'CompanyContactList', params: { companyId: this.companyId } }).href"></BackLinkButton>
        <PageHeader>Create Contact</PageHeader>
        <Form>
            <InlineFieldGroup>
                <InlineField label="First Name">
                    <Input id="first_name" v-model="model.first_name"></Input>
                </InlineField>
                <InlineField label="Last Name">
                    <Input id="last_name" v-model="model.last_name"></Input>
                </InlineField>
            </InlineFieldGroup>

            <Field label="E-Mail">
                <Input id="email" v-model="model.email" type="email"></Input>
            </Field>
            <Field label="Phone">
                <Input id="phone" v-model="model.phone"></Input>
            </Field>
            <Field label="Role">
                <Input id="role" v-model="model.role"></Input>
            </Field>
            <Field label="PGP Public Key">
                <Textarea id="pgp_public_key" v-model="model.pgp_public_key"></Textarea>
            </Field>
            <Button class="w-full" @click="create">Save</Button>
        </Form>
    </ContainerLayout>
</template>
