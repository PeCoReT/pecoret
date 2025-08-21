<script>
import { BlankSlate } from '@/components/blankslate';
import { CommentCard } from '@/partials/common';
import { MarkdownEditor } from '@/components/editor';
import { FindingTabMenu } from '@/partials/projects';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'FindingCommentList',
    data() {
        return {
            loading: false,
            findingId: this.$route.params.findingId,
            projectId: this.$route.params.projectId,
            model: {
                comment: ''
            },
            items: [],
            newComment: null,
            saveCommentLoading: false
        };
    },
    methods: {
        getComments() {
            this.loading = true;
            this.$api
                .get(this.$api.e.pFindingCommentList, { pPk: this.projectId, fPk: this.findingId })
                .then((response) => {
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        patchComment(pk, comment) {
            let data = { comment: comment };
            this.$api
                .patch(
                    this.$api.e.pFindingCommentDetail,
                    {
                        pPk: this.projectId,
                        fPk: this.findingId,
                        pk: pk
                    },
                    data
                )
                .then(() => {
                    this.getComments();
                });
        },
        saveComment() {
            this.saveCommentLoading = true;
            this.$api
                .post(
                    this.$api.e.pFindingCommentList,
                    {
                        pPk: this.projectId,
                        fPk: this.findingId
                    },
                    { comment: this.newComment }
                )
                .then((response) => {
                    this.$toaster({
                        title: 'Created!',
                        duration: 3000,
                        description: 'Comment created!'
                    });
                    this.$emit('object-created', response.data);
                    this.newComment = null;
                    this.getComments();
                })
                .finally(() => {
                    this.saveCommentLoading = false;
                });
        }
    },
    mounted() {
        this.getComments();
    },
    components: { ContainerLayout, MarkdownEditor, CommentCard, BlankSlate, FindingTabMenu, Button }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <FindingTabMenu></FindingTabMenu>
        </template>
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

        <div class="p-4">
            <Form>
                <Field label="Add a comment">
                    <MarkdownEditor v-model="newComment"></MarkdownEditor>
                </Field>
                <Button class="w-full" @click="saveComment">Submit</Button>
            </Form>
        </div>
    </ContainerLayout>
</template>
