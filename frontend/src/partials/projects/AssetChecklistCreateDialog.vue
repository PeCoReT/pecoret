<script>
import { AssetSelectField } from '@/partials/projects';
import { ModalDialog } from '@/components/dialog';
import {Button} from '@/components/ui/button';
import ModelCombobox from "@/components/combobox/ModelCombobox.vue";
import {Select} from '@/components/select';

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
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            let data = {
                asset: this.model.asset,
                checklist_id: this.model.checklist
            };
            this.$api.post(this.$api.e.pChecklistList, { projectPk: this.projectId }, data).then((response) => {
                this.$toaster({
                    title: 'Created',
                    duration: 3000,
                    detail: 'Checklist created successfully!'
                });
                this.$emit('object-created', response.data);
                this.showDialog = false;
            });
        },
    },
    components: {ModelCombobox, ModalDialog, AssetSelectField, Button, Select }
};
</script>

<template>

    <ModalDialog v-model="showDialog" v-model:loading="loading" header="New Checklist" @onSave="create">
        <template #trigger>
            <Button>
                <i class="fa fa-plus"></i> Checklist
            </Button>
        </template>
        <Form>
            <Field label="Asset">
                <ModelCombobox v-model="model.asset" label="" variant="form" :api-endpoint="this.$api.e.pAssetList" :url-args="{pPk: projectId}" @select=""></ModelCombobox>
            </Field>
            <Field label="Checklist">
                <ModelCombobox v-model="model.checklist" :api-endpoint="this.$api.e.checklistList" variant="form" value-field="checklist_id"></ModelCombobox>
            </Field>
        </Form>
    </ModalDialog>
</template>
