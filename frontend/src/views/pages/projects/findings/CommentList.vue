<script>
import markdown from '@/utils/markdown';
import FindingTabMenu from '@/components/navigation/FindingTabMenu.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import FindingCommentFormDialog from '@/components/projects/findings/FindingCommentFormDialog.vue';
import CommentCard from '@/components/cards/CommentCard.vue';

export default {
    name: 'FindingCommentList',
    props: {
        findingId: {
            required: true
        },
        projectId: {
            required: true
        }
    },
    data() {
        return {
            loading: false,
            model: {
                comment: ''
            },
            items: [],
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'FindingList',
                        params: { projectId: this.projectId }
                    })
                },
                {
                    label: 'Finding Detail',
                    to: this.$router.resolve({
                        name: 'FindingDetail',
                        params: { projectId: this.projectId, findingId: this.findingId }
                    })
                },
                {
                    label: 'Comments',
                    disabled: true
                }
            ]
        };
    },
    methods: {
        renderMarkdown(text) {
            return markdown.renderMarkdown(text);
        },
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
        getUserEditUsername(comment) {
            if (comment.user_edit) {
                return comment.user_edit.username;
            }
            return comment.user_edit;
        }
    },
    mounted() {
        this.$api.get(this.$api.e.pFindingDetail, { pPk: this.projectId, pk: this.findingId }).then((response) => {
            this.breadcrumbs[this.breadcrumbs.length - 2] = {
                label: response.data.unique_id,
                to: this.$router.resolve({
                    name: 'FindingDetail',
                    params: { projectId: this.projectId, findingId: this.findingId }
                })
            };
        });
        this.getComments();
    },
    components: { CommentCard, FindingCommentFormDialog, BlankSlate, FindingTabMenu }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid grid-cols-2 space-y-3">
        <div class="col-span-1">
            <div class="justify-start flex"></div>
        </div>
        <div class="col-span-1">
            <div class="flex justify-end">
                <FindingCommentFormDialog @object-created="getComments" :findingId="findingId" :projectId="projectId"></FindingCommentFormDialog>
            </div>
        </div>
    </div>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <FindingTabMenu class="surface-card"></FindingTabMenu>
            <div class="card border-noround-top" v-if="items.length > 0">
                <CommentCard
                    :comment="comment.comment"
                    :date="comment.date_created"
                    :editedBy="getUserEditUsername(comment)"
                    :author="comment.user.username"
                    v-for="comment in items"
                    :key="comment.pk"
                    @comment-edited="
                        (editedComment) => {
                            patchComment(comment.pk, editedComment);
                        }
                    "
                ></CommentCard>
            </div>
            <div class="card border-noround-top" v-else>
                <BlankSlate title="No comments" text="No comments found!" icon="fa fa-comments"></BlankSlate>
            </div>
        </div>
    </div>
</template>
