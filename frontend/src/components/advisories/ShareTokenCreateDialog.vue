<script>
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import AdvisoryService from "@/service/AdvisoryService";

export default {
    name: 'ShareTokenCreateDialog',
    components: { ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                date_expire: null
            },
            loading: false,
            service: new AdvisoryService(),
            advisoryId: this.$route.params.advisoryId
        }
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.service.createShareToken(this.advisoryId, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Token created!',
                    life: 3000,
                    detail: 'Token created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            })
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Share Token" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Share Token" v-model="showDialog" @onSave="create">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText v-model="model.name" id="name"></InputText>
            </div>
            <div class="field col-12">
                <label for="date_expire">Date Expire?</label>
                <Calendar v-model="model.date_expire" id="date_expire"></Calendar>
            </div>
        </div>
    </ModalDialog>
</template>
