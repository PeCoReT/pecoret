<script>
import ASMonitorService from '@/service/ASMonitorService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';

export default {
    name: 'TargetMetaCreateDialog',
    components: { ModalDialog, MarkdownEditor },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            loading: false,
            model: {
                key: null,
                value: null
            },
            service: new ASMonitorService(),
            programId: this.$route.params.programId,
            targetId: this.$route.params.targetId
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        save() {
            this.loading = true;
            this.service
                .createTargetMeta(this.$api, this.programId, this.targetId, this.model)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Target Meta created!',
                        life: 3000,
                        detail: 'Target meta created successfully!'
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
    <Button icon="fa fa-plus" label="Target Meta" outlined @click="open"></Button>
    <ModalDialog :loading="loading" header="Create Target Meta" v-model="showDialog" @onSave="save">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="key">Key</label>
                <InputText v-model="model.key" id="key"></InputText>
            </div>
            <div class="field col-12">
                <label for="value">Value</label>
                <MarkdownEditor v-model="model.value"></MarkdownEditor>
            </div>
        </div>
    </ModalDialog>
</template>
