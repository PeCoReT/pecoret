<script>
import { ModalDialog } from '@/components/dialog';
import { Input } from '@/components/ui/input';
import {DatePicker} from '@/components/datepicker';
import {Button} from '@/components/ui/button';

export default {
    name: 'VersionHistoryCreateDialog',
    emits: ['object-created'],
    components: { ModalDialog, Input, DatePicker, Button },
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            model: {
                version: null,
                change: null,
                date: null
            },
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
                change: this.model.change,
                date: this.model.date,
                version: this.model.version
            };
            this.$api
                .post(
                    this.$api.e.pReportVersionHistoryList,
                    {
                        pPk: this.projectId,
                        rPk: this.reportId
                    },
                    data
                )
                .then((response) => {
                    this.$toaster({
                        title: 'Version added!',
                        duration: 3000,
                        detail: 'Version added to report!'
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
        <i class="fa fa-plus"></i> Change History
    </Button>

    <ModalDialog v-model="visible" v-model:loading="loading" header="Add Change" @onSave="create">
        <Form>
            <Field label="Version">
                <Input id="version" v-model="model.version"></Input>
            </Field>
            <Field label="Change">
                <Input id="change" v-model="model.change"></Input>
            </Field>
            <Field label="Date">
                <DatePicker v-model="model.date"></DatePicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
