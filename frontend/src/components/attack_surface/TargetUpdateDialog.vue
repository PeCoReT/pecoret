<script>
import ASMonitorService from '@/service/ASMonitorService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import TagSelectField from '@/components/asmonitor/TagSelectField.vue';
import TechnologyService from '@/service/TechnologyService';
import ProgramSelectField from '@/components/attack_surface/fields/ProgramSelectField.vue';

export default {
    name: 'TargetUpdateDialog',
    components: { ProgramSelectField, TagSelectField, ModalDialog, MarkdownEditor },
    emits: ['object-updated'],
    props: {
        target: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: this.target,
            loading: false,
            service: new ASMonitorService(),
            techService: new TechnologyService(),
            technologyChoices: [],
            technologies: []
        };
    },
    watch: {
        target: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
                if (value.technologies && this.technologies.length < 1) {
                    for (let i = 0; i < value.technologies.length; i++) {
                        this.technologies.push(value.technologies[i].pk);
                    }
                }
                this.technologyChoices = value.technologies;
            }
        }
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        onTechnologyFilter(event) {
            let data = {
                search: event.value
            };
            this.techService.getTechnologies(this.$api, data).then((response) => {
                this.technologyChoices = response.data.results;
            });
        },
        getTechnologies() {
            this.techService.getTechnologies(this.$api).then((response) => {
                this.technologyChoices = response.data.results;
            });
        },
        patch() {
            this.loading = true;
            let data = {
                description: this.model.description,
                data_type: this.model.data_type,
                scope: this.model.scope,
                tags: this.model.tags,
                technologies: this.technologies,
                data: this.model.data
            };
            if (this.model.tags.length > 0 && this.model.tags[0].pk) {
                delete data.tags;
            }
            this.service
                .patchTarget(this.$api, this.target.pk, data)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Target updated!',
                        life: 3000,
                        detail: 'Target updated successfully!'
                    });
                    this.$emit('object-updated');
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
    <Button icon="fa fa-edit" size="small" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="Update Target" v-model="showDialog" @onSave="patch">
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
