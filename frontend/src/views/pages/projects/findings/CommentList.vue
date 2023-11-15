<script>
import markdown from '@/utils/markdown';
import FindingService from '@/service/FindingService';
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import BlankSlate from "@/components/BlankSlate.vue";

export default {
    name: 'FindingCommentList',
    data() {
        return {
            findingId: this.$route.params.findingId,
            projectId: this.$route.params.projectId,
            findingService: new FindingService(),
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
                        params: { projectId: this.$route.params.projectId }
                    })
                },
                {
                    label: 'Finding Detail',
                    to: this.$router.resolve({
                        name: 'FindingDetail',
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
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
            this.findingService
                .getComments(this.projectId, this.findingId)
                .then((response) => {
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        saveNewComment() {
            let data = {
                comment: this.model.comment
            };
            this.findingService.createComment(this.$api, this.projectId, this.findingId, data).then(() => {
                this.model.comment = '';
                this.getComments();
            });
        }
    },
    mounted() {
        this.getComments();
    },
    components: { BlankSlate, MarkdownEditor, FindingTabMenu }
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
            <FindingTabMenu class="surface-card"></FindingTabMenu>
            <div class="card border-noround-top" v-if="items.length > 1">
                <div class="card pb-3 pt-4" v-for="comment in items" :key="comment.pk">
                    <div class="grid pt-2">
                        <div class="col-12">
                            {{ comment.comment }}
                        </div>
                    </div>
                    <div class="grid text-color-secondary">
                        <div class="col-12">
                            <small>{{ comment.user.username }} - {{ comment.date_created }}</small>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card border-noround-top" v-else>
                <BlankSlate title="No comments" text="No comments found!" icon="fa fa-comments"></BlankSlate>
            </div>
            <div class="card">
                <MarkdownEditor v-model="model.comment"></MarkdownEditor>
                <div class="flex justify-content-end">
                    <Button @click="saveNewComment" label="Save"></Button>
                </div>
            </div>
        </div>
    </div>
</template>