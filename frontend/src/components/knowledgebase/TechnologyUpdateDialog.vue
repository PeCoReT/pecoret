<script>
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TechnologyService from '@/service/TechnologyService';

export default {
    name: 'TechnologyUpdateDialog',
    components: { MarkdownEditor, ModalDialog },
    emits: ['object-updated'],
    props: {
        technology: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: this.technology,
            loading: false,
            service: new TechnologyService()
        };
    },
    watch: {
        technology: {
            immediate: true,
            deep: true,
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
                description: this.model.description,
                cpe: this.model.cpe,
                homepage: this.model.homepage,
                source_code_url: this.model.source_code_url,
                vendor: this.model.vendor
            };
            this.service.patchTechnology(this.$api, this.technology.pk, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Technology updated!',
                    life: 3000,
                    detail: 'Technology updated successfully!'
                });
                this.$emit('object-updated');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-edit" outlined @click="open" size="small"></Button>
    <ModalDialog v-model:loading="loading" header="Update Technology" v-model="showDialog" @onSave="patch">
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
                <label for="vendor">Vendor</label>
                <InputText v-model="model.vendor"></InputText>
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
