<script>

export default {
    name: 'FileDrop',
    emits: ['onFileUpload'],
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
        onSelectedFiles(event) {
            this.uploadFileLoading = true;
            let data = new FormData();
            data.append('image', event.files[event.files.length - 1]);
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
        onTemplatedUpload() {
            this.$toast.add({ severity: 'info', summary: 'Success', detail: 'File Uploaded', life: 3000 });
        },
        copyLinkToClipboard(attachment) {
            let md_data = '![' + attachment.name + '](' + attachment.image + ')';
            navigator.clipboard.writeText(md_data);
            this.$toast.add({
                severity: 'info',
                summary: 'Copied to clipboard',
                detail: 'Link copied to clipboard',
                life: 2000
            });
        }
    }
};
</script>
<template>
    <FileUpload name="demo[]" @upload="onTemplatedUpload($event)" :multiple="true" accept="image/*" :maxFileSize="1000000" @select="onSelectedFiles">
        <template #header="{ chooseCallback }">
            <div class="flex flex-row">
                <div class="flex-col">
                    <Button @click="chooseCallback()" icon="fa fa-upload pl-4 pr-4" outlined :disabled="uploadFileLoading" :loading="uploadFileLoading"></Button>
                </div>
            </div>
        </template>
        <template #content="">
            <Skeleton v-if="attachmentsLoading === true"></Skeleton>
            <div v-if="attachments.length > 0">
                <div class="flex flex-wrap gap-3">
                    <div v-for="file in attachments" :key="file.pk" class="card flex flex-col justify-center align-center gap-3 h-full ml-3 mr-3 border rounded-xl">
                        <div @click="copyLinkToClipboard(file)" class="flex justify-center align-center">
                            <img role="presentation" :alt="file.name.substring(0, 32)" :src="file.image" width="50" height="50" class="shadow-2" />
                        </div>
                        <span class="font-semibold">{{ file.name.substring(0, 32) }}</span>
                        <Button @click="deleteAttachment(file)" label="Delete Attachment" class="p-0 m-0" link severity="danger"></Button>
                    </div>
                </div>
            </div>
            <div v-else class="flex items-center justify-center flex-col">
                <i class="pi pi-cloud-upload border rounded-full p-5 text-8xl text-400 border-400" />
                <p class="mt-4 mb-0">Drag and drop files to here to upload.</p>
            </div>
        </template>
    </FileUpload>
</template>
