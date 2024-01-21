<script>
import CompanyService from '@/service/CompanyService';

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
            companyId: this.$route.params.companyId,
            service: new CompanyService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
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
            this.service.patchContact(this.$api, this.companyId, this.company.pk, data).then(() => {
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

    <Dialog header="Update Contact" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12 md:col-6">
                <label for="first_name">First Name</label>
                <InputText id="first_name" type="text" v-model="model.first_name"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="last_name">Last Name</label>
                <InputText id="last_name" type="text" v-model="model.last_name"></InputText>
            </div>
            <div class="field col-12">
                <label for="email">E-Mail</label>
                <InputText id="email" v-model="model.email" type="email"></InputText>
            </div>
            <div class="field col-12">
                <label for="phone">Phone</label>
                <InputText id="phone" v-model="model.phone"></InputText>
            </div>
            <div class="field col-12">
                <label for="role">Role</label>
                <InputText id="role" v-model="model.role"></InputText>
            </div>
            <div class="field col-12">
                <label for="pgp_public_key">PGP Public Key</label>
                <Textarea id="pgp_public_key" v-model="model.pgp_public_key"></Textarea>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
