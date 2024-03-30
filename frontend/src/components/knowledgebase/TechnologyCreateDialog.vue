<script>
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyService from '@/service/TechnologyService';

export default {
    name: 'TechnologyCreateDialog',
    components: { MarkdownEditor, ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                description: null,
                cpe: null,
                homepage: null,
                source_code_url: null
            },
            loading: false,
            service: new TechnologyService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.service.createTechnology(this.$api, this.model).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Technology created!',
                    life: 3000,
                    detail: 'Technology created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Technology" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="New Technology" v-model="showDialog" @onSave="create">
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText v-model="model.name" id="name"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="cpe">CPE</label>
                <InputText v-model="model.cpe" id="cpe"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="homepage">Homepage</label>
                <InputText v-model="model.homepage"></InputText>
            </div>
            <div class="field col-12">
                <label for="source_code_url">Source Code URL</label>
                <InputText v-model="model.source_code_url"></InputText>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <MarkdownEditor v-model="model.description" id="description"></MarkdownEditor>
            </div>
        </div>
    </ModalDialog>
</template>

<style scoped></style>
