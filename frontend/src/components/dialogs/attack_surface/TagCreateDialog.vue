<script>
import ASMonitorService from '@/service/ASMonitorService';
import ModalDialog from '@/components/common/ModalDialog.vue';

export default {
    name: 'TagCreateDialog',
    components: { ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                description: null,
                color: null
            },
            loading: false,
            service: new ASMonitorService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            let data = {
                name: this.model.name,
                description: this.model.description,
                color: `#${this.model.color}`
            };
            this.service.createTag(this.$api, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Tag created!',
                    life: 3000,
                    detail: 'Tag created successfully'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Tag" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" header="New Tag" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name" id="name"></InputText>
            </Field>
            <Field label="Description">
                <InputText id="description" maxlength="254" v-model="model.description"></InputText>
            </Field>
            <Field label="Color">
                <ColorPicker v-model="model.color"></ColorPicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
