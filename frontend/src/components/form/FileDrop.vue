<script>
import { Button } from '@/components/ui/button';

export default {
    name: 'FileDrop',
    emits: ['onFileUpload'],
    components: { Button },
    data() {
        return {
            attachments: [],
            totalSize: 0,
            totalSizePercent: 0,
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            attachmentsLoading: false,
            uploadFileLoading: false
        };
    },
    mounted() {
        this.getAttachments();
    },
    methods: {
        getAttachments() {
            this.attachmentsLoading = true;
            this.$api
                .get(this.$api.e.pFindingAttachmentList, { pPk: this.projectId, fPk: this.findingId })
                .then((response) => {
                    this.attachments = response.data.results;
                })
                .finally(() => {
                    this.attachmentsLoading = false;
                });
        },
        uploadFile(event) {
            this.uploadFileLoading = true;
            let data = new FormData();
            data.append('image', event.target.files[0]);
            this.$api
                .post(
                    this.$api.e.pFindingAttachmentList,
                    {
                        pPk: this.projectId,
                        fPk: this.findingId
                    },
                    data,
                    { 'Content-Type': 'multipart/form-data' }
                )
                .then((response) => {
                    this.attachments.push(response.data);
                })
                .finally(() => {
                    this.uploadFileLoading = false;
                });
        },
        triggerFileUpload() {
            this.$refs.fileInput.click();
        },
        deleteAttachment(file) {
            this.$api
                .delete(this.$api.e.pFindingAttachmentDetail, {
                    pPk: this.projectId,
                    fPk: this.findingId,
                    pk: file.pk
                })
                .then(() => {
                    this.getAttachments();
                });
        },
        copyLinkToClipboard(attachment) {
            let md_data = '![' + attachment.name + '](' + attachment.image + ')';
            navigator.clipboard.writeText(md_data);
            this.$toaster({
                title: 'Copied to clipboard',
                description: 'Link copied to clipboard',
                duration: 2000
            });
        }
    }
};
</script>
<template>
<div class="flex flex-col w-full border-input border rounded p-3 bg-background">
    <div class="flex justify-start mb-4">
        <Button :disabled="uploadFileLoading" :loading="uploadFileLoading" icon="fa fa-upload pl-4 pr-4" variant="outline" @click="triggerFileUpload">
            <i class="fa fa-upload"></i>
        </Button>
        <input id="dropzone-file" type="file" class="hidden" @change="uploadFile" ref="fileInput" />
    </div>
    <div v-if="attachments.length > 0" class="flex flex-wrap gap-3">
        <div v-for="file in attachments" :key="file.pk" class="p-2 flex flex-col justify-center items-center gap-3 h-full border rounded-xl" @click="copyLinkToClipboard(file)">
            <div class="flex justify-center items-center" @click="copyLinkToClipboard(file)">
                <img :alt="file.name.substring(0, 32)" :src="file.image" class="shadow-2" height="50" role="presentation" width="50" />
            </div>
            <span class="text-sm font-semibold">{{ file.name.substring(0, 32) }}</span>
            <Button class="p-0 m-0" variant="ghost" size="small" @click="deleteAttachment(file)"><span class="text-xs">Delete</span></Button>
        </div>
    </div>
    <div v-else class="flex items-center justify-center flex-col">
        <i class="fa fa-paperclip p-3 text-4xl"></i>
        <p class="mt-2 mb-0">No Attachments</p>
    </div>
</div>

</template>
