<script>
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import TechnologyService from '@/service/TechnologyService';
import ASMonitorService from '@/service/ASMonitorService';
import ProgramSelectField from '@/components/attack_surface/fields/ProgramSelectField.vue';
import TagSelectField from '@/components/asmonitor/TagSelectField.vue';

export default {
    name: 'URLCreateDialog',
    components: { TagSelectField, ProgramSelectField, ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                program: null,
                url: null,
                tags: null,
                technologies: null
            },
            service: new ASMonitorService(),
            techService: new TechnologyService(),
            technologies: [],
            loading: false
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
            this.service.createURL(this.$api, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'URL created!',
                    life: 3000,
                    detail: 'URL created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="URL" outlined @click="open"></Button>
    <ModalDialog :loading="loading" header="New URL" v-model="showDialog" @onSave="create">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="url">URL</label>
                <InputText v-model="model.url"></InputText>
            </div>
            <div class="field col-12">
                <label for="program">Program</label>
                <ProgramSelectField v-model="model.program"></ProgramSelectField>
            </div>
            <div class="field col-12">
                <label for="technologies">Technologies</label>
                <MultiSelect id="technologies" filter @filter="onTechnologyFilter" @focus="getTechnologies" v-model="model.technologies" :options="technologies" optionLabel="name" optionValue="pk"></MultiSelect>
            </div>
            <div class="field col-12">
                <label for="tags">Tags</label>
                <TagSelectField v-model="model.tags"></TagSelectField>
            </div>
        </div>
    </ModalDialog>
</template>

<style scoped></style>
