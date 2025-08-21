<script>
import { MarkdownEditor } from '@/components/editor';
import { ModalDialog } from '@/components/dialog';
import { Input } from '@/components/ui/input';
import {DatePicker} from '@/components/datepicker';

export default {
    name: 'CommandUpdate',
    props: {
        command: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.command,
            loading: false,
            projectId: this.$route.params.projectId
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
                command: this.model.command,
                output: this.model.output,
                date_run: this.model.date_run
            };
            this.$api
                .patch(
                    this.$api.e.pCommandDetail,
                    {
                        projectPk: this.projectId,
                        pk: this.command.pk
                    },
                    data
                )
                .then(() => {
                    this.$emit('object-updated', this.model);
                    this.visible = false;
                });
        }
    },
    watch: {
        command: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    components: { MarkdownEditor, ModalDialog, Input, DatePicker }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" outlined size="small" @click="open"></Button>

    <ModalDialog v-model="visible" v-model:loading="loading" header="Update Command" @onSave="patch">
        <Form>
            <Field label="Command">
                <Input id="name" v-model="model.command" type="text"></Input>
            </Field>
            <Field label="Output">
                <MarkdownEditor v-model="model.output"></MarkdownEditor>
            </Field>
            <Field label="Date run?">
                <DatePicker id="date_expire" v-model="model.date_run"></DatePicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
