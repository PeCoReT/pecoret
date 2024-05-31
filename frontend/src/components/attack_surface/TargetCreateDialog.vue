<script>
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import ASMonitorService from '@/service/ASMonitorService';
import TechnologyService from '@/service/TechnologyService';
import TagSelectField from '@/components/asmonitor/TagSelectField.vue';
import ProgramSelectField from '@/components/attack_surface/fields/ProgramSelectField.vue';

export default {
    name: 'TargetCreateDialog',
    components: { ProgramSelectField, TagSelectField, MarkdownEditor, ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                data: null,
                scope: 'Undefined',
                program: null,
                description: null,
                technologies: null,
                tags: null
            },
            loading: false,
            service: new ASMonitorService(),
            techService: new TechnologyService(),
            technologies: []
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        getTechnologies() {
            this.techService.getTechnologies(this.$api).then((response) => {
                this.technologies = response.data.results;
            });
        },
        onTechnologyFilter(event) {
            let data = {
                search: event.value
            };
            this.techService.getTechnologies(this.$api, data).then((response) => {
                this.technologies = response.data.results;
            });
        },
        create() {
            if (this.model.tags === null) {
                this.model.tags = [];
            }
            if (this.model.technologies === null) {
                this.model.technologies = [];
            }
            this.service.createTarget(this.$api, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Target created!',
                    life: 3000,
                    detail: 'Target created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Target" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Target" v-model="showDialog" @onSave="create">
        <div class="p-fluid grid formgrid">
            <div class="field col-12 md:col-6">
                <label for="name">Data</label>
                <InputText v-model="model.data" id="data"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="ip">Data Type</label>
                <Dropdown :options="service.getDataTypeChoices()" optionLabel="name" optionValue="value" v-model="model.data_type"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="program">Program</label>
                <ProgramSelectField v-model="model.program"></ProgramSelectField>
            </div>
            <div class="field col-12">
                <label for="scope">Scope</label>
                <Dropdown :options="service.getInScopeChoices()" optionLabel="name" optionValue="value" v-model="model.scope"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="technologies">Technologies</label>
                <MultiSelect id="technologies" filter @filter="onTechnologyFilter" @focus="getTechnologies" v-model="model.technologies" :options="technologies" optionLabel="name" optionValue="pk"></MultiSelect>
            </div>
            <div class="field col-12">
                <label for="tags">Tags</label>
                <TagSelectField v-model="model.tags"></TagSelectField>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <MarkdownEditor v-model="model.description" id="description"></MarkdownEditor>
            </div>
        </div>
    </ModalDialog>
</template>
