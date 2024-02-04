<script>
import AdvisoryService from '@/service/AdvisoryService';
import AdvisoryTabMenu from '../../../components/pages/AdvisoryTabMenu.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import AdvisoryCommentCreateDialog from '@/components/advisories/AdvisoryCommentCreateDialog.vue';
import CommentCard from '@/components/elements/CommentCard.vue';

export default {
    name: 'CommentList',
    data() {
        return {
            service: new AdvisoryService(),
            comment: '',
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Advisory Detail',
                    to: this.$router.resolve({
                        name: 'AdvisoryDetail',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Comments',
                    disabled: true
                }
            ],
            advisoryId: this.$route.params.advisoryId,
            items: []
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.service.getComments(this.$api, this.advisoryId).then((response) => {
                this.items = response.data.results;
            });
        },
        patchComment(pk, comment) {
            let data = { comment: comment };
            this.service.patchComment(this.$api, this.advisoryId, pk, data).then(() => {
                this.getItems();
            });
        },
        getUserEditUsername(comment) {
            if (comment.user_edit) {
                return comment.user_edit.username;
            }
            return comment.user_edit;
        }
    },
    components: { CommentCard, AdvisoryCommentCreateDialog, AdvisoryTabMenu, BlankSlate }
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
            <div class="justify-content-start flex"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <AdvisoryCommentCreateDialog :advisory-id="this.advisoryId" @object-created="getItems"></AdvisoryCommentCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <AdvisoryTabMenu class="surface-card"></AdvisoryTabMenu>
            <div class="card border-noround-top" v-if="items.length > 0">
                <CommentCard
                    :comment="comment.comment"
                    :date="comment.date_created"
                    :author="comment.user.username"
                    :editedBy="getUserEditUsername(comment)"
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
