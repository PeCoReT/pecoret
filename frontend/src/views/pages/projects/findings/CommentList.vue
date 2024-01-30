<script>
import markdown from '@/utils/markdown';
import FindingService from '@/service/FindingService';
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import FindingCommentFormDialog from '@/components/projects/findings/FindingCommentFormDialog.vue';

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
            service: new FindingService(),
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
            this.service
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
            this.service.createComment(this.$api, this.projectId, this.findingId, data).then(() => {
                this.model.comment = '';
                this.getComments();
            });
        }
    },
    mounted() {
        this.service.getFinding(this.projectId, this.findingId).then((response) => {
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
    components: { FindingCommentFormDialog, BlankSlate, FindingTabMenu }
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
                <FindingCommentFormDialog @object-created="getComments" :findingId="findingId" :projectId="projectId"></FindingCommentFormDialog>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <FindingTabMenu class="surface-card"></FindingTabMenu>
            <div class="card border-noround-top" v-if="items.length > 0">
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
        </div>
    </div>
</template>
