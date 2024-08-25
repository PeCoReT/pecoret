<script>
import FindingService from '@/service/FindingService';
import TechnologySelectField from '@/components/forms/fields/TechnologySelectField.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';

export default {
    name: 'FindingAsAdvisoryDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            loading: false,
            model: {
                technology: null,
                affected_versions: null
            },
            service: new FindingService()
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.loading = true;
            let data = {
                technology: this.model.technology,
                affected_versions: this.model.affected_versions
            };
            this.service
                .findingAsAdvisory(this.$api, this.projectId, this.findingId, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Finding copies as advisory!',
                        life: 3000,
                        detail: 'Finding was successfully copied as advisory!'
                    });
                    this.$emit('object-created', response.data);
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { ModalDialog, TechnologySelectField }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Finding As Advisory" outlined @click="open"></Button>
    <ModalDialog v-model:loading="loading" header="Finding as Advisory" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Product">
                <TechnologySelectField v-model="model.technology"></TechnologySelectField>
            </Field>
            <Field label="Affected Versions">
                <InputText v-model="model.affected_versions"></InputText>
            </Field>
        </Form>
    </ModalDialog>
</template>
