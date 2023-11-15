<script>
import PBreadcrumb from '@/components/Breadcrumb.vue';
import ProjectNoteService from '@/service/ProjectNoteService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import { useAuthStore } from '@/store/auth';

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
            saveLoading: false,
            previousSelected: null,
            authStore: useAuthStore()
        };
    },
    computed: {
        showMessage() {
            if (this.selectedNote !== null && this.selectedNote.object_lock !== null) {
                if (this.selectedNote.object_lock.user.username !== this.authStore.me.username) {
                    return true;
                }
            }
            return false;
        }
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
            let data = { title: title, text: '' };
            if (this.selectedNote !== null && this.selectedNote.object_lock !== null) {
                this.service.unlockNote(this.$api, this.projectId, this.selectedNote.pk).then(() => {
                    this.selectedNote = null;
                });
            }
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
            this.saveLoading = true;
            let data = {
                title: this.selectedNote.title,
                text: this.selectedNote.text
            };
            this.service
                .patchNote(this.$api, this.projectId, this.selectedNote.pk, data)
                .then(() => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Saved',
                        detail: 'Note was saved!',
                        life: 3000
                    });
                    this.getNotes();
                })
                .finally(() => {
                    this.saveLoading = false;
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
        },
        patchLock() {
            this.service.lockNote(this.$api, this.projectId, this.selectedNote.pk).then(() => {});
        },
        onNoteSelected(event) {
            if (event.value === null) {
                this.selectedNote = null;
                return;
            }
            this.getNotes();
            for (let i = 0; i < this.notes.length; i++) {
                if (this.notes[i].pk === event.value.pk) {
                    this.selectedNote = this.notes[i];
                    if (this.selectedNote.object_lock === null) {
                        this.service.lockNote(this.$api, this.projectId, this.selectedNote.pk).then((response) => {
                            this.notes[i] = response.data;
                        });
                    }
                } else {
                    if (this.notes[i].object_lock !== null && this.notes[i].object_lock.user.username === this.authStore.me.username) {
                        this.service.unlockNote(this.$api, this.projectId, this.notes[i].pk).then(() => {
                            this.notes[i].object_lock = null;
                        });
                    }
                }
            }
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
                <Button icon="fa fa-plus" label="Note" outlined @click="createNote"></Button>
                <Button icon="fa fa-trash" label="Delete" outlined severity="danger" @click="deleteNote" :disabled="!selectedNote"></Button>
            </div>
        </div>
    </div>
    <Message v-if="showMessage" :closable="false">Object is locked by user {{ this.selectedNote.object_lock.user.username }}! </Message>

    <div class="card">
        <div class="grid">
            <div class="col-3 h-full">
                <Listbox @change="onNoteSelected" v-model="selectedNote" :options="notes" filter @filter="onListFilter" optionLabel="title" class="w-full">
                    <template #option="slotProps">
                        <div class="flex align-items-center">
                            <div>
                                {{ slotProps.option.title }}
                                <Button class="m-0 p-0" icon="fa fa-lock" text :disabled="true" v-if="slotProps.option.object_lock !== null"></Button>
                                <small v-if="slotProps.option.object_lock !== null">
                                    <i>{{ slotProps.option.object_lock.user.username }}</i>
                                </small>
                            </div>
                        </div>
                    </template>
                </Listbox>
            </div>
            <div class="col-9">
                <div class="grid formgrid p-fluid">
                    <div class="col-12 field">
                        <InputText v-model="selectedNote.title" v-if="selectedNote !== null"></InputText>
                    </div>
                    <div class="col-12 field">
                        <MarkdownEditor v-if="selectedNote !== null" v-model="selectedNote.text" @update:modelValue="patchLock"></MarkdownEditor>
                    </div>
                    <div class="col-12 field">
                        <Button label="Save" @click="patchNote" :loading="saveLoading" v-if="selectedNote !== null"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>