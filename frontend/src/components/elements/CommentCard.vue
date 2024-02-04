<script>
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'CommentCard',
    props: {
        author: {
            required: true
        },
        date: {
            required: true
        },
        comment: {
            required: true
        },
        editedBy: {
            required: false
        }
    },
    emit: ['comment-edited'],
    data() {
        return {
            editMode: false,
            editedComment: this.comment,
            items: [
                {
                    label: 'Edit',
                    icon: 'fa fa-edit',
                    command: () => {
                        this.editMode = !this.editMode;
                    }
                }
            ]
        };
    },
    methods: {
        toggle(event) {
            this.$refs.menu.toggle(event);
        },
        onCommentEdited() {
            this.$emit('comment-edited', this.editedComment);
            this.editMode = false;
        }
    },
    components: { MarkdownEditor }
};
</script>

<template>
    <Card class="card p-0 surface-ground border-200 border-1 border-round mt-3">
        <template #header>
            <div class="col-12 surface-card border-bottom-1 border-200">
                <div class="grid">
                    <div class="col-10">
                        <div class="flex justify-content-start">{{ author }} commented on {{ date }}</div>
                    </div>
                    <div class="col-2">
                        <div class="flex justify-content-end">
                            <Button size="small" text type="button" class="text-color p-1" icon="fa fa-ellipsis" @click="toggle" aria-haspopup="true" aria-controls="comment_edit_menu" />
                            <Menu ref="menu" id="comment_edit_menu" :model="items" :popup="true"></Menu>
                        </div>
                    </div>
                    <div class="col-12 mt-0 pt-0 pb-0 mb-0" v-if="editedBy">
                        <small>edited by {{ editedBy }}</small>
                    </div>
                </div>
            </div>
        </template>
        <template #content>
            <div class="grid">
                <div class="col-12" v-if="editMode !== true">
                    {{ comment }}
                </div>
                <div class="col-12" v-else>
                    <MarkdownEditor v-model="editedComment"></MarkdownEditor>
                    <Button label="Save" @click="onCommentEdited"></Button>
                </div>
            </div>
        </template>
    </Card>
</template>
