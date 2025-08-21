<script>
import { ModalDialog } from '@/components/dialog';
import { Input } from '@/components/ui/input';
import {Button} from '@/components/ui/button';
import {Select} from '@/components/select';

export default {
    name: 'ReportDocumentCreateDialog',
    emits: ['object-created'],
    components: { ModalDialog, Input, Button, Select },
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            loading: false,
            model: {
                name: null,
                release_type: null
            },
            releaseTypeChoices: [
                { label: 'Draft', value: 'Draft' },
                { label: 'Final', value: 'Final' }
            ]
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
                name: this.model.name,
                release_type: this.model.release_type
            };
            this.$api
                .post(
                    this.$api.e.pReportDocumentList,
                    {
                        pPk: this.projectId,
                        rPk: this.reportId
                    },
                    data
                )
                .then((response) => {
                    this.$toaster({
                        title: 'Document created!',
                        duration: 3000,
                        detail: 'New document created!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                });
        }
    }
};
</script>

<template>
    <Button @click="open">
        <i class="fa fa-plus"></i> Document
    </Button>

    <ModalDialog v-model="visible" v-model:loading="loading" header="Create Document" @onSave="create">
        <Form>
            <Field label="Name">
                <Input id="name" v-model="model.name"></Input>
            </Field>
            <Field label="Release Type">
                <Select id="release_type" v-model="model.release_type" :options="releaseTypeChoices" optionLabel="title" optionValue="value"></Select>
            </Field>
        </Form>
    </ModalDialog>
</template>
