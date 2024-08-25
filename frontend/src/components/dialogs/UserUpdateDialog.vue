<script>
import AdminService from '@/service/AdminService';
import CompanySelectField from '@/components/forms/fields/CompanySelectField.vue';

export default {
    name: 'UserUpdateDialog',
    components: { CompanySelectField },
    props: {
        user: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.user,
            service: new AdminService(),
            groupChoices: [],
            customerGroupId: null,
            loading: false
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
            this.getGroups();
        },
        patch() {
            let data = {
                username: this.model.username,
                first_name: this.model.first_name,
                last_name: this.model.last_name,
                email: this.model.email,
                groups: this.model.groups,
                is_active: this.model.is_active
            };
            if (this.isCustomerSelected === true) {
                data['company'] = this.model.company;
            }
            this.service.patchUser(this.$api, this.user.pk, data).then(() => {
                this.$emit('object-updated', this.model);
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
    },
    watch: {
        user: {
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

    <ModalDialog header="Update User" v-model="visible" :loading="loading" @onSave="patch">
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
            <Field label="Is Active?">
                <ToggleSwitch v-model="model.is_active"></ToggleSwitch>
            </Field>
        </Form>
    </ModalDialog>
</template>
