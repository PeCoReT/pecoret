<script>
import ASMonitorService from '@/service/ASMonitorService';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';

export default {
    name: 'ScopeCreateDialog',
    components: { ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            loading: false,
            model: {
                scope_type: null,
                data: null
            },
            service: new ASMonitorService(),
            programId: this.$route.params.programId
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        save() {
            this.loading = true;
            this.service
                .createScope(this.$api, this.programId, this.model)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'scope created!',
                        life: 3000,
                        detail: 'Scope created successfully!'
                    });
                    this.$emit('object-created');
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Scope" outlined @click="open"></Button>
    <ModalDialog :loading="loading" header="Create Scope" v-model="showDialog" @onSave="save">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="type">Scope Type</label>
                <Dropdown :options="service.getScopeTypeChoices()" v-model="model.scope_type" optionLabel="name" optionValue="value"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="data">Data</label>
                <InputText v-model="model.data"></InputText>
            </div>
        </div>
    </ModalDialog>
</template>
