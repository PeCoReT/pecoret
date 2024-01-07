<script>
import AuthService from '@/service/AuthService';

export default {
    name: 'ChangePasswordDialog',
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: {
                old_password: null,
                new_password: null
            },
            service: new AuthService()
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
            this.service.changePassword(this.$api, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'Password changed!'
                });
                this.$emit('object-updated', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Dialog header="Create API-Token" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </div>
            <div class="field col-12">
                <label for="date_expire">Date Expire?</label>
                <Calendar v-model="model.date_expire" id="date_expire"></Calendar>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
