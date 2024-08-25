<script>
import CompanyService from '@/service/CompanyService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'CompanyInformationCreateDialog',
    props: {
        companyId: {
            required: true
        }
    },
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            companyService: new CompanyService(),
            text: '',
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
        create() {
            let data = {
                text: this.text
            };
            this.companyService.createCompanyInformation(this.$api, this.companyId, data).then(() => {
                this.$toast.add({ severity: 'success', summary: 'Created!', detail: 'Company Information created!', life: 3000 });
                this.$emit('object-created');
                this.visible = false;
            });
        }
    },
    components: { MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Company Information" @click="open" outlined></Button>

    <ModalDialog header="Create Company Information" v-model="visible" :loading="loading" @onSave="create">
        <Form>
            <Field label="Text">
                <MarkdownEditor v-model="text"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>