<script>
import ModalDialog from '@/components/common/ModalDialog.vue';

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
            advisoryId: this.$route.params.advisoryId
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.$api.post(this.$api.e.aShareTokenList, { aPk: this.advisoryId }, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Token created!',
                    life: 3000,
                    detail: 'Token created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Share Token" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Share Token" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name"></InputText>
            </Field>
            <Field label="Date Expire?">
                <DatePicker v-model="model.date_expire"></DatePicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
