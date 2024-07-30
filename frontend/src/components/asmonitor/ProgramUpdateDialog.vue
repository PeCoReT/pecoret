<script>
import ASMonitorService from '@/service/ASMonitorService';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';


export default {
    name: 'ProgramUpdateDialog',
    components: { ModalDialog, MarkdownEditor },
    props: {
        program: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            showDialog: false,
            model: this.program,
            loading: false,
            service: new ASMonitorService()
        };
    },
    watch: {
        program: {
            deep: true,
            immediate: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                description: this.model.description
            };
            this.service.patchProgram(this.$api, this.program.pk, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Program updated!',
                    life: 3000,
                    detail: 'Program updated successfully'
                });
                this.$emit('object-updated');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-edit" label="Program" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" header="Update Program" v-model="showDialog" @onSave="patch">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText v-model="model.name" id="name"></InputText>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <MarkdownEditor id="description" v-model="model.description"></MarkdownEditor>
            </div>
        </div>
    </ModalDialog>
</template>
