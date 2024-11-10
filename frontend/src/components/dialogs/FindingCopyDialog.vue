<script>
import ModalDialog from '@/components/common/ModalDialog.vue';

export default {
    name: 'FindingCopyDialog',
    components: { ModalDialog },
    emits: ['object-created'],
    props: {
        finding: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            projectId: this.$route.params.projectId,
            loading: false,
            model: {
                name: null
            },
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            let data = {
                name: this.model.name
            };
            this.$api.post(this.$api.e.pFindingCopy, { pPk: this.projectId, pk: this.finding }, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Finding copied!',
                    life: 3000,
                    detail: 'Finding copied successfully!'
                });
                this.$emit('object-created', response.data);
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-copy" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="Copy Finding" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name"></InputText>
            </Field>
        </Form>
    </ModalDialog>
</template>
