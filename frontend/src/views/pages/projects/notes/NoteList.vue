<script>
import PBreadcrumb from '@/components/Breadcrumb.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import { useAuthStore } from '@/store/auth';
import RenderedNote from '@/components/projects/notes/RenderedNote.vue';

export default {
    name: 'NoteList',
    components: { RenderedNote, MarkdownEditor, PBreadcrumb },
    data() {
        return {
            breadcrumbs: [{ label: 'Notes', disabled: true }],
            selectedNote: null,
            notes: [],
            projectId: this.$route.params.projectId,
            saveLoading: false,
            previousSelected: null,
            authStore: useAuthStore(),
            pagination: { limit: 25, page: 1 },
            totalRecords: 0,
            editMode: false,
            timer: ''
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
    beforeUnmount() {
        if (this.selectedNote) {
            this.$api
                .delete(this.$api.e.pNoteUnlock, { projectPk: this.projectId, pk: this.selectedNote.pk })
                .then(() => {})
                .catch(() => {});
            this.stopTimerUpdate();
        }
    },
    methods: {
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getNotes();
        },
        getNotes() {
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.$api.get(this.$api.e.pNoteList, { projectPk: this.projectId }, params).then((response) => {
                this.notes = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        createNote() {
            this.saveLoading = true;
            let title = 'New Note ' + new Date().getTime();
            let data = { title: title, text: '' };
            this.$api
                .post(this.$api.e.pNoteList, { projectPk: this.projectId }, data)
                .then((response) => {
                    this.selectedNote = response.data;
                    this.getNotes();
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
            this.$api
                .patch(this.$api.e.pNoteDetail, { projectPk: this.projectId, pk: this.selectedNote.pk }, data)
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
                    this.$api
                        .delete(this.$api.e.pNoteDetail, {
                            projectPk: this.projectId,
                            pk: this.selectedNote.pk
                        })
                        .then(() => {
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
            this.$api.get(this.$api.e.pNoteList, { projectPk: this.projectId }, params).then((response) => {
                this.notes = response.data.results;
            });
        },
        patchLock() {
            this.$api
                .post(this.$api.e.pNoteLock, {
                    projectPK: this.projectId,
                    pk: this.selectedNote.pk
                })
                .then((resp) => {
                    this.selectedNote.object_lock = resp.data.object_lock;
                    for (let i = 0; i < this.notes.length; i++) {
                        if (this.notes[i].pk === this.selectedNote.pk) {
                            this.notes[i] = this.selectedNote;
                        }
                    }
                });
        },
        startTimerUpdate() {
            // reload data every 5s
            this.timer = setInterval(this.patchLock, 5 * 1000);
        },
        stopTimerUpdate() {
            clearInterval(this.timer);
            this.timer = null;
        },
        enterEditMode() {
            this.editMode = true;
            this.patchLock();
            this.startTimerUpdate();
        },
        exitEditMode() {
            this.editMode = false;
            this.$api
                .delete(this.$api.e.pNoteUnlock, {
                    projectPk: this.projectId,
                    pk: this.selectedNote.pk
                })
                .then(() => {
                    for (let i = 0; i < this.notes.length; i++) {
                        if (this.notes[i].pk === this.selectedNote.pk) {
                            this.notes[i].object_lock = null;
                        }
                    }
                    this.selectedNote.object_lock = null;
                });
            this.stopTimerUpdate();
        },
        onNoteSelected(event) {
            if (event.value === null) {
                this.selectedNote = null;
                return;
            }
            if (this.editMode === true) {
                // do not allow action when in edit mode
                return;
            }
            this.getNotes();
            for (let i = 0; i < this.notes.length; i++) {
                if (this.notes[i].pk === event.value.pk) {
                    this.selectedNote = this.notes[i];
                    break;
                } else {
                    if (this.notes[i].object_lock !== null && this.notes[i].object_lock.user.username === this.authStore.me.username) {
                        this.$api
                            .delete(this.$api.e.pNoteUnlock, {
                                projectPk: this.projectId,
                                pk: this.notes[i].pk
                            })
                            .then(() => {
                                this.notes[i].object_lock = null;
                                this.stopTimerUpdate();
                            });
                    }
                }
            }
        }
    }
};
</script>
<template>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-6">
            <div class="flex justify-start"></div>
        </div>
        <div class="col-span-6">
            <div class="flex justify-end space-x-2">
                <Button icon="fa fa-plus" label="Note" outlined @click="createNote" v-if="!this.editMode"></Button>
                <Button icon="fa fa-edit" label="Edit" outlined @click="enterEditMode" :disabled="!selectedNote" v-if="!this.editMode"></Button>
                <Button icon="fa fa-close" label="Exit" outlined @click="exitEditMode" :disabled="!selectedNote" v-else></Button>
                <Button icon="fa fa-trash" label="Delete" outlined severity="danger" @click="deleteNote" :disabled="!selectedNote" v-if="!this.editMode"></Button>
            </div>
        </div>
    </div>
    <Message v-if="showMessage" :closable="false">Object is locked by user {{ this.selectedNote.object_lock.user.username }}! </Message>

    <div class="card mt-3">
        <div class="grid grid-cols-12 gap-4">
            <div class="col-span-3 h-full">
                <Listbox @change="onNoteSelected" v-model="selectedNote" :options="notes" filter @filter="onListFilter" optionLabel="title" class="w-full" :disabled="this.editMode">
                    <template #option="slotProps">
                        <div class="flex items-center">
                            <div>
                                {{ slotProps.option.title }}
                                <Button class="m-0 p-0" icon="fa fa-lock" text :disabled="true" v-if="slotProps.option.object_lock !== null"></Button>
                                <small v-if="slotProps.option.object_lock">
                                    <i>{{ slotProps.option.object_lock.user.username }}</i>
                                </small>
                            </div>
                        </div>
                    </template>
                </Listbox>
                <Paginator :rows="pagination.limit" :totalRecords="totalRecords" @page="onPage"></Paginator>
            </div>
            <div class="col-span-9">
                <RenderedNote :note="selectedNote" v-if="selectedNote !== null && editMode === false"></RenderedNote>

                <div v-if="editMode === true && selectedNote !== null">
                    <div class="grid grid-cols-12 gap-4">
                        <div class="col-span-12">
                            <InputText class="w-full" v-model="selectedNote.title" v-if="selectedNote !== null"></InputText>
                        </div>
                        <div class="col-span-12">
                            <MarkdownEditor v-if="selectedNote !== null" v-model="selectedNote.text"></MarkdownEditor>
                        </div>
                        <div class="col-span-12">
                            <Button class="w-full" label="Save" @click="patchNote" :loading="saveLoading" v-if="selectedNote !== null"></Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
