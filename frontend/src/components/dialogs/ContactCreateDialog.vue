<script>
import CompanyService from '@/service/CompanyService';

export default {
    name: 'ContactCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            companyService: new CompanyService(),
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
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        create() {
            let data = {
                first_name: this.model.first_name,
                last_name: this.model.last_name,
                phone: this.model.phone,
                pgp_public_key: this.model.pgp_public_key,
                email: this.model.email,
                role: this.model.role
            };
            this.companyService.createContact(this.$api, this.companyId, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    detail: 'Contact created for company!',
                    life: 3000
                });
                this.$emit('object-created');
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Contact" @click="open" outlined></Button>

    <ModalDialog header="Create Contact" v-model="visible" :loading="loading" @onSave="create">
        <Form>
            <InlineFieldGroup>
                <InlineField label="First Name">
                    <InputText id="first_name" v-model="model.first_name"></InputText>
                </InlineField>
                <InlineField label="Last Name">
                    <InputText id="last_name" v-model="model.last_name"></InputText>
                </InlineField>
            </InlineFieldGroup>

            <Field label="E-Mail">
                <InputText id="email" v-model="model.email" type="email"></InputText>
            </Field>
            <Field label="Phone">
                <InputText id="phone" v-model="model.phone"></InputText>
            </Field>
            <Field label="Role">
                <InputText id="role" v-model="model.role"></InputText>
            </Field>
            <Field label="PGP Public Key">
                <Textarea id="pgp_public_key" v-model="model.pgp_public_key"></Textarea>
            </Field>
        </Form>
    </ModalDialog>
</template>
