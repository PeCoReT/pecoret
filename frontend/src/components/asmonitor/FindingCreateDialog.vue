<script>
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import ASMonitorService from '@/service/ASMonitorService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import SeveritySelectField from '@/components/elements/forms/SeveritySelectField.vue';
import VulnerabilityService from '@/service/VulnerabilityService';
import TagSelectField from '@/components/asmonitor/TagSelectField.vue';

export default {
    name: 'FindingCreateDialog',
    components: { TagSelectField, MarkdownEditor, ModalDialog, SeveritySelectField },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                severity: null,
                cwe: null,
                proof_text: null,
                target: null,
                tags: null
            },
            targetChoices: null,
            cweChoices: null,
            loading: false,
            service: new ASMonitorService(),
            vulnService: new VulnerabilityService(),
            programId: this.$route.params.programId
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        getTargets() {
            this.service.getTargets(this.$api, this.programId).then((response) => {
                this.targetChoices = response.data.results;
            });
        },
        onFilterTarget(event) {
            let params = {
                search: event.value
            };
            this.service.getTargets(this.$api, this.programId, params).then((response) => {
                this.targetChoices = response.data.results;
            });
        },
        onFilterCWE(event) {
            let params = {
                search: event.value
            };
            this.vulnService.getCWEs(this.$api, params).then((response) => {
                this.cweChoices = response.data.results;
            });
        },
        getCWEchoices() {
            this.vulnService.getCWEs(this.$api).then((response) => {
                this.cweChoices = response.data.results;
            });
        },
        create() {
            this.service.createFinding(this.$api, this.programId, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Program created!',
                    life: 3000,
                    detail: 'Program created successfully!'
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
                <label for="target">Target</label>
                <Dropdown id="target" filter optionLabel="name" optionValue="pk" :options="targetChoices" v-model="model.target" @filter="onFilterTarget" @focus="getTargets"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="cwe">CWE-ID</label>
                <Dropdown id="cwe" filter optionLabel="name" optionValue="pk" :options="cweChoices" v-model="model.cwe" @filter="onFilterCWE" @focus="getCWEchoices"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="tags">Tags</label>
                <TagSelectField v-model="model.tags"></TagSelectField>
            </div>
            <div class="field col-12">
                <label for="description">Proof</label>
                <MarkdownEditor v-model="model.proof_text"></MarkdownEditor>
            </div>
        </div>
    </ModalDialog>
</template>
