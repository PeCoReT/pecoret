<script>
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'CommentCard',
    components: { MarkdownEditor },
    props: {
        comment: {
            required: true
        }
    },
    emits: ['onDelete', 'onEdit'],
    methods: {
        menuToggle(event) {
            this.$refs.menu.toggle(event);
        },
        onCommentEdited() {
            this.$emit('onEdit', this.editedComment);
            this.editMode = false;
        }
    },
    data() {
        return {
            editedComment: this.comment,
            editMode: false,
            menuItems: [
                {
                    label: 'Edit',
                    icon: 'fa fa-edit',
                    command: () => {
                        this.editMode = !this.editMode;
                    }
                },
                {
                    label: 'Delete',
                    icon: 'fa fa-trash',
                    command: () => {
                        this.$emit('onDelete', this.comment);
                    }
                }
            ]
        };
    }
};
</script>

<template>
    <div class="border rounded-xl p-5 border-gray-700">
        <div class="flex justify-between items-center">
            <div class="flex items-center">
                <p class="inline-flex items-center mr-3 text-sm text-white font-semibold">
                    {{ comment.user.username }}
                </p>
                <p class="text-sm text-gray-400">{{ comment.date_created }}</p>
            </div>
            <Button size="small" text icon="fa fa-ellipsis-vertical" class="!text-gray-400 !p-0 !m-0" @click="menuToggle"></Button>
            <Menu :model="menuItems" :popup="true" ref="menu"></Menu>
        </div>
        <div v-if="comment.user_edit">
            <p class="text-sm text-gray-400">
                edited by <strong class="font-semibold text-white">{{ comment.user_edit.username }}</strong>
            </p>
        </div>
        <p class="text-gray-400 mt-3 markdown-block" v-html="comment.text_md" v-if="editMode !== true"></p>
        <div v-else>
            <Form>
                <Field>
                    <MarkdownEditor v-model="editedComment.text"></MarkdownEditor>
                </Field>
                <Button label="Save" class="w-full" @click="onCommentEdited"></Button>
            </Form>
        </div>
    </div>
</template>
