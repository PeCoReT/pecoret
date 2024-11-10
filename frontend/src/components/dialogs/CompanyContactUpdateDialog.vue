<script>

export default {
    name: 'CompanyContactUpdateDialog',
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
            loading: false,
            companyId: this.$route.params.companyId,
        };
    },
    methods: {
        open() {
            this.visible = true;
        },
        patch() {
            let data = {
                first_name: this.model.first_name,
                last_name: this.model.last_name,
                phone: this.model.phone,
                pgp_public_key: this.model.pgp_public_key,
                email: this.model.email,
                role: this.model.role
            };
            this.$api.patch(this.$api.e.cContactDetail, { cPk: this.companyId, pk: this.company.pk }, data).then(() => {
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
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>
    <ModalDialog header="Update Contact" v-model="visible" :loading="loading" @onSave="patch">
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
