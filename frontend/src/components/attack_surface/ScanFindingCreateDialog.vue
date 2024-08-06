<script>
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import ASMonitorService from '@/service/ASMonitorService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import SeveritySelectField from '@/components/elements/forms/SeveritySelectField.vue';
import TagSelectField from '@/components/asmonitor/TagSelectField.vue';
import ProgramSelectField from '@/components/attack_surface/fields/ProgramSelectField.vue';

export default {
    name: 'ScanFindingCreateDialog',
    components: { ProgramSelectField, TagSelectField, MarkdownEditor, ModalDialog, SeveritySelectField },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                severity: null,
                tool: null,
                program: null,
                affected_component: null,
                tags: null,
                description: null,
                comment: null,
                full_output: null
            },
            targetChoices: null,
            cweChoices: null,
            loading: false,
            service: new ASMonitorService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            if (this.model.tags === null) {
                this.model.tags = [];
            }
            this.service.createScanFinding(this.$api, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Finding created!',
                    life: 3000,
                    detail: 'Finding created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Finding" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Finding" v-model="showDialog" @onSave="create">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText v-model="model.name" id="name"></InputText>
            </div>
            <div class="field col-12">
                <SeveritySelectField v-model="model.severity"></SeveritySelectField>
            </div>
            <div class="field col-12">
                <label for="tool">Tool</label>
                <InputText v-model="model.tool" id="tool"></InputText>
            </div>
            <div class="field col-12">
                <label for="program">Program</label>
                <ProgramSelectField v-model="model.program"></ProgramSelectField>
            </div>
            <div class="field col-12">
                <label for="component">Affected Component</label>
                <InputText v-model="model.affected_component"></InputText>
            </div>
            <div class="field col-12">
                <label for="tags">Tags</label>
                <TagSelectField v-model="model.tags"></TagSelectField>
            </div>
            <div class="field col-12">
                <label for="description">Result</label>
                <MarkdownEditor v-model="model.result"></MarkdownEditor>
            </div>
            <div class="field col-12">
                <label for="comment">Full Output</label>
                <MarkdownEditor v-model="model.full_output"></MarkdownEditor>
            </div>
        </div>
    </ModalDialog>
</template>
