<script>
import { Breadcrumb } from '@/components/breadcrumb';
import { MarkdownEditor } from '@/components/editor';
import { useAuthStore } from '@/store/auth';
import { RenderedNote } from '@/partials/projects';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { ExclamationTriangleIcon } from '@radix-icons/vue';
import { Paginator } from '@/components/paginator';
import { Input } from '@/components/ui/input';
import SearchField from '@/partials/common/SearchField.vue';
import { Button } from '@/components/ui/button';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'NoteList',
    mixins: [listViewMixin],
    components: {
        SearchField,
        RenderedNote,
        MarkdownEditor,
        Breadcrumb,
        Alert,
        AlertDescription,
        AlertTitle,
        ExclamationTriangleIcon,
        Paginator,
        Input,
        Button
    },
    data() {
        return {
            selectedNote: null,
            notes: [],
            projectId: this.$route.params.projectId,
            saveLoading: false,
            previousSelected: null,
            authStore: useAuthStore(),
            editMode: false,
            filters: {
                search: { value: null }
            }
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
        this.getItems();
    },
    methods: {
        getItems(params) {
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api.get(this.$api.e.pNoteList, { projectPk: this.projectId }, data).then((response) => {
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
                    this.getItems();
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
                    this.$toaster({
                        title: 'Saved',
                        description: 'Note was saved!',
                        duration: 3000
                    });
                    this.getItems();
                })
                .finally(() => {
                    this.saveLoading = false;
                });
        },
        deleteNote() {
            this.$confirm.require({
                message: 'Do you want to delete this note?',
                accept: () => {
                    this.$api
                        .delete(this.$api.e.pNoteDetail, {
                            projectPk: this.projectId,
                            pk: this.selectedNote.pk
                        })
                        .then(() => {
                            this.$toaster({
                                title: 'Deleted',
                                description: 'Note was deleted!',
                                duration: 3000
                            });
                            this.getItems();
                            this.selectedNote = null;
                        });
                }
            });
        },
        patchLock() {
            this.$api
                .post(this.$api.e.pNoteLock, {
                    projectPk: this.projectId,
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
        enterEditMode() {
            this.editMode = true;
            this.patchLock();
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
        },
        onNoteSelected(event) {
            this.editMode = false;
            if (event === null) {
                this.selectedNote = null;
                return;
            }
            if (this.editMode === true) {
                // do not allow action when in edit mode
                return;
            }
            this.getItems();
            for (let i = 0; i < this.notes.length; i++) {
                if (this.notes[i].pk === event.pk) {
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
                            });
                    }
                }
            }
        }
    }
};
</script>
<template>
    <div class="grid grid-cols-12 mt-12">
        <div class="col-span-6">
            <div class="flex justify-start"></div>
        </div>
        <div class="col-span-6">
            <div class="flex justify-end space-x-2">
                <Button v-if="!this.editMode" @click="createNote"><i class="fa fa-plus"></i> Note</Button>
                <Button v-if="!this.editMode" :disabled="!selectedNote" variant="outline" @click="enterEditMode"><i
                        class="fa fa-edit"></i> Edit </Button>
                <Button v-else :disabled="!selectedNote" variant="outline" @click="exitEditMode"><i
                        class="fa fa-close"></i> Unlock </Button>
                <Button v-if="!this.editMode" :disabled="!selectedNote" variant="destructive" @click="deleteNote"><i
                        class="fa fa-trash"></i> Delete </Button>
            </div>
        </div>
    </div>
    <Alert v-if="showMessage" class="mt-3" variant="destructive">
        <ExclamationTriangleIcon class="w-4 h-4" />
        <AlertTitle>Locked</AlertTitle>
        <AlertDescription>Object is locked by user {{ this.selectedNote.object_lock.user.username }}!</AlertDescription>
    </Alert>

    <div class="card mt-3">
        <div class="grid grid-cols-12 gap-4">
            <div class="col-span-3 h-full">
                <div class="bg-card rounded-lg p-1 w-full border">
                    <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
                    <ul class="space-y-1 mt-1">
                        <li v-for="note in notes" :key="note.pk"
                            :class="{ 'bg-muted': selectedNote && selectedNote.pk === note.pk }"
                            class="p-2 rounded hover:bg-accent hover:cursor-pointer" @click="
                                () => {
                                    this.onNoteSelected(note);
                                }
                            ">
                            {{ note.title }}
                            <span v-if="note.object_lock">
                                <i class="fa fa-lock"></i>
                                <small class="ml-2">by {{ note.object_lock.user.username }}</small>
                            </span>
                        </li>
                        <li v-if="notes.length < 1" class="p-2 rounded hover:bg-accent hover:cursor-pointer">No
                            available options</li>
                    </ul>
                </div>
                <Paginator :rows="pagination.limit" :totalRecords="totalRecords" class="mt-3 flex justify-center"
                    @page="onPage"></Paginator>
            </div>
            <div class="col-span-9">
                <RenderedNote v-if="selectedNote !== null && editMode === false" :note="selectedNote"></RenderedNote>

                <div v-if="editMode === true && selectedNote !== null">
                    <div class="grid grid-cols-12 gap-4">
                        <div class="col-span-12">
                            <Input v-if="selectedNote !== null" v-model="selectedNote.title" class="w-full"></Input>
                        </div>
                        <div class="col-span-12">
                            <MarkdownEditor v-if="selectedNote !== null" v-model="selectedNote.text"></MarkdownEditor>
                        </div>
                        <div class="col-span-12">
                            <Button v-if="selectedNote !== null" class="w-full" @click="patchNote">Save</Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
