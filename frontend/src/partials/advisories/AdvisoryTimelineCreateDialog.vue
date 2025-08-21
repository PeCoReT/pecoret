<script>
import { ModalDialog } from '@/components/dialog';
import { Input } from '@/components/ui/input';
import {DatePicker} from '@/components/datepicker';

export default {
    name: 'AdvisoryTimelineCreateDialog',
    components: { ModalDialog, Input, DatePicker },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            advisoryId: this.$route.params.advisoryId,
            model: {
                text: null,
                date: null
            },
            loading: false
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.loading = true;
            let data = {
                text: this.model.text
            };
            if (this.model.date) {
                data['date'] = this.model.date.toISOString().split('T')[0];
            }
            this.$api
                .post(this.$api.e.aTimelineList, { aPk: this.advisoryId }, data)
                .then((response) => {
                    this.$toaster({
                        title: 'Timeline added!',
                        duration: 3000,
                        description: 'Timeline added to Advisory!'
                    });
                    this.$emit('object-created', response.data);
                    this.showDialog = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Timeline" outlined @click="open"></Button>

    <ModalDialog v-model="showDialog" :loading="loading" header="Create Timeline Entry" @onSave="create">
        <Form>
            <Field label="Text">
                <Input v-model="model.text"></Input>
            </Field>
            <Field label="Date">
                <DatePicker v-model="model.date"></DatePicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
