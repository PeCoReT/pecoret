<script>
import { MarkdownEditor } from '@/components/editor';
import { ModalDialog } from '@/components/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { DatePicker } from '@/components/datepicker';

export default {
    name: 'ProjectCommandCreate',
    emits: ['object-created'],
    components: { MarkdownEditor, ModalDialog, Button, Input, DatePicker },
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            loading: false,
            model: {
                command: null,
                output: null,
                date_run: null
            }
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
            this.$api.post(this.$api.e.pCommandList, { projectPk: this.projectId }, this.model).then((response) => {
                this.$toaster({
                    title: 'Created!',
                    duration: 3000,
                    detail: 'Command created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button @click="open"><i class="fa fa-plus" /> Command</Button>

    <ModalDialog v-model="visible" v-model:loading="loading" header="Create Command" @onSave="create">
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
