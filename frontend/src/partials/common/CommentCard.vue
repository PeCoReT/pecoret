<script>
import { MarkdownEditor } from '@/components/editor';
import renderMarkdown from '@/lib/markdown';
import { Button } from '@/components/ui/button';

export default {
    name: 'CommentCard',
    props: {
        comment: {
            required: true
        }
    },
    emit: ['comment-edited'],
    data() {
        return {
            editMode: false,
            editedComment: this.comment.comment || this.comment.text
        };
    },
    methods: {
        onCommentEdited() {
            this.$emit('comment-edited', this.editedComment);
            this.editMode = false;
        },
        renderMarkdown,
        toggleEdit() {
            this.editMode = !this.editMode;
        },
        getUserEditUsername(comment) {
            if (comment.user_edit) {
                return comment.user_edit.username;
            }
            return comment.user_edit;
        }
    },
    components: { MarkdownEditor, Button }
};
</script>

<template>
    <div class="mb-2">
        <div class="border-b py-3 border p-3 rounded-xl">
            <div class="flex justify-between items-center">
                <div class="flex items-center">
                    <div>
                        <span class="text-foreground font-semibold">{{ comment.user.username }}</span>
                        <span class="text-muted-foreground text-xs ml-2">{{ comment.date_created }}</span>
                    </div>
                </div>
                <div class="flex justify-end">
                    <Button size="small" variant="ghost" @click="toggleEdit"><i class="fa fa-edit" />Edit</Button>
                    <Button class="p-0 m-0" icon="fa fa-edit" label="Edit" outlined size="small" variant="link" @click="toggleEdit"></Button>
                </div>
            </div>
            <div v-if="!editMode">
                <p v-if="!editMode && comment.comment" class="text-muted-foreground mt-2" v-html="renderMarkdown(comment.comment)"></p>
                <p v-if="!editMode && comment.text" class="text-muted-foreground mt-2" v-html="renderMarkdown(comment.text)"></p>
                <p v-if="getUserEditUsername(comment)" class="text-muted-foreground text-sm mt-2">Edited by {{ getUserEditUsername(comment) }}</p>
            </div>
            <div v-else>
                <MarkdownEditor v-model="editedComment" class="mt-3"></MarkdownEditor>
                <Button class="w-full mt-3" @click="onCommentEdited">Save</Button>
            </div>
        </div>
    </div>
</template>
