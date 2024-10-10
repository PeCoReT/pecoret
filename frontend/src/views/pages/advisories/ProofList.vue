<script>
import AdvisoryService from '@/service/AdvisoryService';
import AdvisoryTabMenu from '@/components/navigation/AdvisoryTabMenu.vue';
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
            this.service.getAdvisory(this.advisoryId).then((response) => {
                this.model = response.data;
            });
        },
        patchAdvisory() {
            let data = {
                proof_text: this.model.proof_text
            };
            this.service.patchAdvisory(this.advisoryId, data).then(() => {
                this.$toast.add({ severity: 'info', summary: 'Updated', detail: 'Proof was updated!', life: 3000 });
            });
        },
        onImageUpload(file, onSuccess) {
            let data = new FormData();
            data.append('image', file);
            this.service.attachmentCreate(this.advisoryId, data).then((resp) => {
                onSuccess(resp.data.storage_link);
            });
        }
    },
    mounted() {
        this.getAdvisory();
    },
    components: { MarkdownEditor, AdvisoryTabMenu }
};
</script>

<template>
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-6">
            <div class="flex justify-start"></div>
        </div>
        <div class="col-span-6">
            <div class="flex justify-end"></div>
        </div>
    </div>
    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <AdvisoryTabMenu></AdvisoryTabMenu>
            <div class="card border-noround-top">
                <Form>
                    <Field label="Text">
                        <MarkdownEditor v-model="model.proof_text" :show-upload-button="true" @upload="onImageUpload"></MarkdownEditor>
                    </Field>

                    <Button label="Save" @click="patchAdvisory" class="w-full"></Button>
                </Form>
            </div>
        </div>
    </div>
</template>
