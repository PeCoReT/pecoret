<script>
import CompanyService from '@/service/CompanyService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'CompanyInformationUpdateDialog',
    props: {
        information: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.information,
            service: new CompanyService(),
            companyId: this.$route.params.companyId,
            loading: false
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        patch() {
            let data = {
                text: this.model.text
            };
            this.service.patchCompanyInformation(this.$api, this.companyId, this.information.pk, data).then(() => {
                this.$emit('object-updated', this.model);
                this.visible = false;
            });
        }
    },
    watch: {
        information: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    components: { MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <ModalDialog header="Update Company Information" v-model="visible" :loading="loading" @onSave="patch">
        <Form>
            <Field label="Text">
                <MarkdownEditor v-model="model.text"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>
