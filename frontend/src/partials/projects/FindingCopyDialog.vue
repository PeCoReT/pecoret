<script>
import { ModalDialog } from '@/components/dialog';
import { Input } from '@/components/ui/input';
import {Button} from '@/components/ui/button';

export default {
    name: 'FindingCopyDialog',
    components: { ModalDialog, Input, Button },
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
            }
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
                this.$toaster({
                    title: 'Finding copied!',
                    duration: 3000,
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
    <Button @click="open" variant="outline"><i class="fa fa-copy"/></Button>
    <ModalDialog v-model="showDialog" v-model:loading="loading" header="Copy Finding" @onSave="create">
        <Form>
            <Field label="Name">
                <Input v-model="model.name"></Input>
            </Field>
        </Form>
    </ModalDialog>
</template>
