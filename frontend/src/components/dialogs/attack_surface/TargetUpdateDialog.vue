<script>
import ASMonitorService from '@/service/ASMonitorService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import TagSelectField from '@/components/forms/fields/TagSelectField.vue';
import TechnologyService from '@/service/TechnologyService';
import ProgramSelectField from '@/components/forms/fields/ProgramSelectField.vue';

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
        <Form>
            <Field label="Data">
                <InputText v-model="model.data" id="data"></InputText>
            </Field>
            <Field label="Data Type">
                <Select :options="service.getDataTypeChoices()" optionLabel="name" optionValue="value" v-model="model.data_type"></Select>
            </Field>
            <Field label="Program">
                <ProgramSelectField v-model="model.program"></ProgramSelectField>
            </Field>
            <Field label="Scope">
                <Select :options="service.getInScopeChoices()" optionLabel="name" optionValue="value" v-model="model.scope"></Select>
            </Field>
            <Field label="Technologies">
                <MultiSelect id="technologies" filter @filter="onTechnologyFilter" @focus="getTechnologies" v-model="model.technologies" :options="technologies" optionLabel="name" optionValue="pk"></MultiSelect>
            </Field>
            <Field label="Tags">
                <TagSelectField v-model="model.tags"></TagSelectField>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description" id="description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
