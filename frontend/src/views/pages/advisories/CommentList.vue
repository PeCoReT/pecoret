<script>
import AdvisoryService from '@/service/AdvisoryService';
import AdvisoryTabMenu from '../../../components/pages/AdvisoryTabMenu.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

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
            items: [],
            activeEditableComment: null
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
        saveNewComment() {
            let data = {
                comment: this.comment
            };
            this.service.createComment(this.$api, this.advisoryId, data).then(() => {
                this.getItems();
                this.comment = '';
            });
        },
        onClickEditComment(comment) {
            this.activeEditableComment = comment;
            this.activeEditableComment.editMode = !this.activeEditableComment.editMode;
            if (!this.activeEditableComment.editMode) {
                this.activeEditableComment = null;
            }
        },
        patchComment(comment) {
            let data = { comment: comment.comment };
            this.service.patchComment(this.$api, this.advisoryId, comment.pk, data);
        }
    },
    components: { AdvisoryTabMenu, MarkdownEditor }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <AdvisoryTabMenu class="surface-card"></AdvisoryTabMenu>
            <div class="card border-noround-top">
                <Card v-for="comment in items" :key="comment.pk" class="surface-ground border-200 border-1 border-round mt-3">
                    <template #header>
                        <div class="col-12 surface-card border-200 border-1 border-round">
                            <div class="grid">
                                <div class="col-10">
                                    <div class="flex justify-content-start">
                                        {{ comment.user.username }} commented on
                                        {{ comment.date_created }}
                                    </div>
                                </div>
                                <div class="col-2">
                                    <div class="flex justify-content-end">
                                        <Button size="small" class="p-1 text-color" text icon="fa fa-ellipsis" @click="onClickEditComment(comment)"></Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template #content>
                        <div class="grid">
                            <div class="col-12" v-if="!comment.editMode">
                                {{ comment.comment }}
                            </div>
                            <div class="col-12" v-else>
                                <MarkdownEditor v-model="comment.comment" @blur="patchComment(comment)"></MarkdownEditor>
                            </div>
                        </div>
                    </template>
                </Card>
            </div>
            <div class="card mt-3" v-if="!this.activeEditableComment">
                <MarkdownEditor v-model="comment"></MarkdownEditor>
                <div class="flex justify-content-end">
                    <Button @click="saveNewComment" label="Save"></Button>
                </div>
            </div>
        </div>
    </div>
</template>