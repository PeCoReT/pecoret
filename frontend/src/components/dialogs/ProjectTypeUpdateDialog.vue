<script>
import AdminService from '@/service/AdminService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ProjectTypeUpdateDialog',
    components: { MarkdownEditor },
    props: {
        pentestType: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.pentestType,
            loading: false,
            service: new AdminService()
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
            this.loading = true;
            let data = {
                name: this.model.name,
                description: this.model.description
            };
            this.service
                .patchProjectType(this.$api, this.pentestType.pk, data)
                .then(() => {
                    this.$emit('object-updated', this.model);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    watch: {
        pentestType: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <ModalDialog header="Update Project Type" v-model="visible" @onSave="patch" :loading="loading">
        <Form>
            <Field label="Name">
                <InputText id="name" v-model="model.name"></InputText>
            </Field>
            <Field label="Description">
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </Field>
        </Form>
    </ModalDialog>
</template>