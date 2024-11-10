<script>
import AssetSelectField from '@/components/forms/fields/AssetSelectField.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';

export default {
    name: 'AssetChecklistCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                asset: null,
                checklist: null
            },
            loading: false,
            projectId: this.$route.params.projectId,
            checklistChoices: [],
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            let data = {
                component: this.model.asset,
                checklist_id: this.model.checklist
            };
            this.$api.post(this.$api.e.pChecklistList, { projectPk: this.projectId }, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created',
                    life: 3000,
                    detail: 'Checklist created successfully!'
                });
                this.$emit('object-created', response.data);
                this.showDialog = false;
            });
        },
        onFocusChecklist() {
            this.$api.get(this.$api.e.checklistList).then((response) => {
                this.checklistChoices = response.data.results;
            });
        },
        onFilterChecklist(event) {
            let params = {
                search: event.value
            };
            this.$api.get(this.$api.e.checklistList, null, params).then((response) => {
                this.checklistChoices = response.data.results;
            });
        }
    },
    components: { ModalDialog, AssetSelectField }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Checklist" @click="open()" outlined></Button>

    <ModalDialog v-model:loading="loading" header="New Checklist" v-model="showDialog" @onSave="create">
        <Form>
            <AssetSelectField v-model="model.asset"></AssetSelectField>
            <Field label="Checklist">
                <Select v-model="model.checklist" :options="checklistChoices" filter @focus="onFocusChecklist" @filter="onFilterChecklist" optionLabel="name" optionValue="checklist_id"></Select>
            </Field>
        </Form>
    </ModalDialog>
</template>
