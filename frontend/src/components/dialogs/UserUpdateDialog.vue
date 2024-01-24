<script>
import AdminService from '@/service/AdminService';
import CompanySelectField from '@/components/elements/forms/CompanySelectField.vue';

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
            this.getGroups();
        },
        patch() {
            let data = {
                username: this.model.username,
                first_name: this.model.first_name,
                last_name: this.model.last_name,
                email: this.model.email,
                groups: this.model.groups
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

    <Dialog header="Update User" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="grid formgrid p-fluid">
            <div class="field col-12">
                <label for="username">Username</label>
                <InputText id="username" v-model="model.username"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="first_name">First Name</label>
                <InputText id="first_name" v-model="model.first_name"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="last_name">Last Name</label>
                <InputText id="last_name" v-model="model.last_name"></InputText>
            </div>
            <div class="field col-12">
                <label for="email">E-Mail</label>
                <InputText id="email" v-model="model.email"></InputText>
            </div>
            <div class="field col-12">
                <label for="groups">Groups</label>
                <MultiSelect id="groups" v-model="model.groups" :options="groupChoices" @focus="getGroups" optionValue="pk" optionLabel="name"></MultiSelect>
            </div>
            <div class="field col-12" v-if="isCustomerSelected === true">
                <label for="company">Company</label>
                <CompanySelectField v-model="model.company"></CompanySelectField>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
