<script>
import PBreadcrumb from '@/components/Breadcrumb.vue';
import ProjectNoteService from '@/service/ProjectNoteService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'NoteList',
    components: { MarkdownEditor, PBreadcrumb },
    data() {
        return {
            breadcrumbs: [{ label: 'Notes', disabled: true }],
            selectedNote: null,
            notes: [],
            projectId: this.$route.params.projectId,
            service: new ProjectNoteService(),
            saveLoading: false
        };
    },
    mounted() {
        this.getNotes();
    },
    methods: {
        getNotes() {
            this.service.getNotes(this.$api, this.projectId).then((response) => {
                this.notes = response.data.results;
            });
        },
        createNote() {
            this.saveLoading = true;
            let title = 'New Note ' + new Date().getTime();
            let data = { title: title };
            this.service
                .createNote(this.$api, this.projectId, data)
                .then((response) => {
                    this.notes.push(response.data);
                    this.selectedNote = response.data;
                })
                .finally(() => {
                    this.saveLoading = false;
                });
        },
        patchNote() {
            let data = {
                title: this.selectedNote.title,
                text: this.selectedNote.text
            };
            this.service.patchNote(this.$api, this.projectId, this.selectedNote.pk, data).then((response) => {
                this.selectedNote = response.data;
                this.getNotes();
            });
        },
        deleteNote() {
            this.$confirm.require({
                message: 'Do you want to delete this note?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteNote(this.$api, this.projectId, this.selectedNote.pk).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Note was deleted!',
                            life: 3000
                        });
                        this.getNotes();
                        this.selectedNote = null;
                    });
                }
            });
        },
        onListFilter(event) {
            let params = {
                search: event.value
            };
            this.service.getNotes(this.$api, this.projectId, params).then((response) => {
                this.notes = response.data.results;
            });
        }
    }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <Button icon="fa fa-save" label="Save" outlined @click="patchNote" :disabled="!selectedNote" :loading="saveLoading"></Button>
                <Button icon="fa fa-plus" label="Note" outlined @click="createNote"></Button>
                <Button icon="fa fa-trash" label="Delete" outlined severity="danger" @click="deleteNote" :disabled="!selectedNote"></Button>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-3 h-full">
            <Listbox v-model="selectedNote" :options="notes" filter @filter="onListFilter" optionLabel="title" class="w-full"></Listbox>
        </div>
        <div class="col-9">
            <div class="grid formgrid p-fluid">
                <div class="col-12 field">
                    <InputText v-model="selectedNote.title" v-if="selectedNote !== null"></InputText>
                </div>
                <div class="col-12 field">
                    <MarkdownEditor v-if="selectedNote !== null" v-model="selectedNote.text"></MarkdownEditor>
                </div>
            </div>
        </div>
    </div>
</template>