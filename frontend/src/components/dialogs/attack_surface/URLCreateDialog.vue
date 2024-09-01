<script>
import ModalDialog from '@/components/common/ModalDialog.vue';
import TechnologyService from '@/service/TechnologyService';
import ASMonitorService from '@/service/ASMonitorService';
import ProgramSelectField from '@/components/forms/fields/ProgramSelectField.vue';
import TagSelectField from '@/components/forms/fields/TagSelectField.vue';

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
        <Form>
            <Field label="URL">
                <InputText v-model="model.url"></InputText>
            </Field>
            <Field label="Program">
                <ProgramSelectField v-model="model.program"></ProgramSelectField>
            </Field>
            <Field label="Technologies">
                <MultiSelect id="technologies" filter @filter="onTechnologyFilter" @focus="getTechnologies" v-model="model.technologies" :options="technologies" optionLabel="name" optionValue="pk"></MultiSelect>
            </Field>
            <Field label="Tags">
                <TagSelectField v-model="model.tags"></TagSelectField>
            </Field>
        </Form>
    </ModalDialog>
</template>

<style scoped></style>
