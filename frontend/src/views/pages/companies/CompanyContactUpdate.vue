<script>
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'CompanyContactUpdate',
    components: { ContainerLayout, Input, Button, Textarea },
    data() {
        return {
            model: {},
            loading: false,
            companyId: this.$route.params.companyId,
            pk: this.$route.params.contactId,
            breadcrumbs: [
                { label: 'Companies', route: this.$router.resolve({ name: 'CompanyList' }) },
                {
                    label: 'Company Detail',
                    route: this.$router.resolve({ name: 'CompanyDetail', params: { pk: this.companyId } })
                },
                {
                    label: 'Update',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.$api.get(this.$api.e.cContactDetail, { cPk: this.companyId, pk: this.pk }).then((response) => {
            this.model = response.data;
        });
    },
    methods: {
        patch() {
            let data = {
                first_name: this.model.first_name,
                last_name: this.model.last_name,
                phone: this.model.phone,
                pgp_public_key: this.model.pgp_public_key,
                email: this.model.email,
                role: this.model.role
            };
            this.$api.patch(this.$api.e.cContactDetail, { cPk: this.companyId, pk: this.pk }, data).then(() => {
                this.$router.push({ name: 'CompanyContactList', params: { companyId: this.companyId } });
            });
        }
    }
};
</script>

<template>
    <ContainerLayout :breadcrumbs="breadcrumbs">
        <h3 class="text-3xl mb-3">Update Contact</h3>
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
            <Button class="w-full" @click="patch">Save</Button>
        </Form>
    </ContainerLayout>
</template>
