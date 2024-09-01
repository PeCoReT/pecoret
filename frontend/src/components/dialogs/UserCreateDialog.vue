<script>
import AdminService from '@/service/AdminService';
import CompanySelectField from '@/components/forms/fields/CompanySelectField.vue';

export default {
    name: 'UserCreateDialog',
    components: { CompanySelectField },
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            model: {
                username: null,
                first_name: null,
                last_name: null,
                email: null,
                groups: [],
                company: null,
                password: null,
                is_active: false
            },
            loading: false,
            service: new AdminService(),
            groupChoices: [],
            customerGroupId: null
        };
    },
    computed: {
        isCustomerSelected() {
            if (this.customerGroupId === null) {
                return false;
            }
            for (let i = 0; i < this.model.groups.length; i++) {
                if (this.model.groups[i] === this.customerGroupId) {
                    return true;
                }
            }
            return false;
        }
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
                username: this.model.username,
                first_name: this.model.first_name,
                last_name: this.model.last_name,
                email: this.model.email,
                groups: this.model.groups,
                password: this.model.password,
                company: this.model.company
            };
            this.service.createUser(this.$api, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'User Created!',
                    life: 3000,
                    detail: 'User created successfully!'
                });
                this.$emit('object-created', response.data);
                this.model.password = null;
                this.visible = false;
            });
        },
        getGroups() {
            this.service.getGroups(this.$api).then((response) => {
                this.groupChoices = response.data.results;
                this.groupChoices.forEach((group) => {
                    if (group.name === 'Customer') {
                        this.customerGroupId = group.pk;
                    }
                });
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="User" outlined @click="open"></Button>

    <ModalDialog header="Create User" v-model="visible" :loading="loading" @onSave="create">
        <Form>
            <Field label="Username">
                <InputText id="username" v-model="model.username"></InputText>
            </Field>
            <InlineFieldGroup>
                <InlineField label="First Name">
                    <InputText id="first_name" v-model="model.first_name"></InputText>
                </InlineField>
                <InlineField label="Last Name">
                    <InputText id="last_name" v-model="model.last_name"></InputText>
                </InlineField>
            </InlineFieldGroup>
            <Field label="E-Mail">
                <InputText id="email" v-model="model.email"></InputText>
            </Field>
            <Field label="Groups">
                <MultiSelect id="groups" v-model="model.groups" :options="groupChoices" @focus="getGroups" optionValue="pk" optionLabel="name"></MultiSelect>
            </Field>
            <Field label="Company" v-if="isCustomerSelected === true">
                <CompanySelectField v-model="model.company"></CompanySelectField>
            </Field>
            <Field label="Password">
                <Password id="password" v-model="model.password" :feedback="false" :toggleMask="true" :pt="{ pcInput: { root: 'grow' } }"></Password>
                <small>You can leave the password empty to send an activation mail to the user! Users where the password was set are inactive by default. Enable them using the update dialog!</small>
            </Field>
        </Form>

    </ModalDialog>
</template>
