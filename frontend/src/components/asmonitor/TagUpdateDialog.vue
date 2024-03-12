<script>
import ASMonitorService from '@/service/ASMonitorService';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';

export default {
    name: 'TagCreateDialog',
    components: { ModalDialog },
    emits: ['object-updated'],
    props: {
        tag: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: this.tag,
            loading: false,
            service: new ASMonitorService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                description: this.model.description,
                color: `#${this.model.color}`
            };
            this.service.patchTag(this.$api, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Tag updated!',
                    life: 3000,
                    detail: 'Tag updated successfully'
                });
                this.$emit('object-updated');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-edit" size="small" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" header="Update Tag" v-model="showDialog" @onSave="patch">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText v-model="model.name" id="name"></InputText>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <InputText id="description" maxlength="254" v-model="model.description"></InputText>
            </div>
            <div class="field col-12">
                <label for="color" class="mr-3">Color</label>
                <ColorPicker v-model="model.color"></ColorPicker>
            </div>
        </div>
    </ModalDialog>
</template>
