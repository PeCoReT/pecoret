<script>
import { AdvisoryTabMenu } from '@/partials/advisories';
import { CommentCard } from '@/partials/common';
import { MarkdownEditor } from '@/components/editor';
import { Button } from '@/components/ui/button';
import { ReloadIcon } from '@radix-icons/vue';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'CommentList',
    data() {
        return {
            comment: '',
            newComment: null,
            saveCommentLoading: false,
            advisoryId: this.$route.params.advisoryId,
            items: []
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.$api.get(this.$api.e.aCommentList, { aPk: this.advisoryId }).then((response) => {
                this.items = response.data.results;
            });
        },
        patchComment(pk, comment) {
            let data = { comment: comment };
            this.$api.patch(this.$api.e.aCommentDetail, { aPk: this.advisoryId, pk: pk }, data).then(() => {
                this.getItems();
            });
        },
        saveComment() {
            this.saveCommentLoading = true;
            this.$api
                .post(this.$api.e.aCommentList, { aPk: this.advisoryId }, { comment: this.newComment })
                .then(() => {
                    this.$toaster({
                        duration: 3000,
                        description: 'Comment created successfully!',
                        title: 'Comment created!'
                    });
                    this.newComment = null;
                    this.getItems();
                })
                .finally(() => {
                    this.saveCommentLoading = false;
                });
        }
    },
    components: { ContainerLayout, ReloadIcon, CommentCard, AdvisoryTabMenu, MarkdownEditor, Button }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <AdvisoryTabMenu></AdvisoryTabMenu>
        </template>
        <div class="col-span-12">
            <CommentCard
                v-for="comment in items"
                :key="comment.pk"
                :comment="comment"
                @comment-edited="
                    (editedComment) => {
                        patchComment(comment.pk, editedComment);
                    }
                "
            ></CommentCard>
            <Form>
                <Field label="Add a comment">
                    <MarkdownEditor v-model="newComment"></MarkdownEditor>
                </Field>
                <Button :disabled="!newComment" class="w-full" @click="saveComment">
                    <ReloadIcon v-if="saveCommentLoading" class="w-4 h-4 mr-2 animate-spin"></ReloadIcon>
                    Submit
                </Button>
            </Form>
        </div>
    </ContainerLayout>
</template>
