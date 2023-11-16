<script>
import AdvisoryService from '@/service/AdvisoryService';
import AdvisoryTabMenu from '@/components/pages/AdvisoryTabMenu.vue';
import AdvisoryAttachmentFileDrop from '@/components/pages/advisories/AdvisoryAttachmentFileDrop.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ProofList',
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
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
                    label: 'Proofs',
                    disabled: true
                }
            ],
            advisoryId: this.$route.params.advisoryId,
            model: {}
        };
    },
    methods: {
        getAdvisory() {
            this.service.getAdvisory(this.$api, this.advisoryId).then((response) => {
                this.model = response.data;
            });
        },
        patchAdvisory() {
            let data = {
                proof_text: this.model.proof_text
            };
            this.service.patchAdvisory(this.$api, this.advisoryId, data).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Updated', detail: 'Proof was updated!', life: 3000 });
            });
        }
    },
    mounted() {
        this.getAdvisory();
    },
    components: { MarkdownEditor, AdvisoryAttachmentFileDrop, AdvisoryTabMenu }
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
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end"></div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <AdvisoryTabMenu class="surface-card"></AdvisoryTabMenu>
            <div class="card border-noround-top">
                <div class="grid formgrid p-fluid">
                    <div class="col-12 field">
                        <MarkdownEditor v-model="model.proof_text"></MarkdownEditor>
                    </div>
                    <div class="col-12 field">
                        <AdvisoryAttachmentFileDrop></AdvisoryAttachmentFileDrop>
                    </div>
                    <div class="col-12 field">
                        <Button label="Save" @click="patchAdvisory"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>