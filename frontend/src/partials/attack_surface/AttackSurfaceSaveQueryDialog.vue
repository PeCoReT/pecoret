<script>
import { ModalDialog } from '@/components/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default {
    name: 'AttackSurfaceSaveQueryDialog',
    emits: ['object-created'],
    components: { ModalDialog, Button, Input },
    props: {
        query: {
            required: true
        }
    },
    data() {
        return {
            visible: false,
            model: {
                name: null
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
                query: this.query,
                name: this.model.name
            };
            this.$api.post(this.$api.e.asSearchQueryList, null, data).then((response) => {
                this.$toaster({
                    title: 'Created!',
                    duration: 3000,
                    description: 'Query created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button :disabled="!this.query" variant="outline" @click="open">Save <i class="fa fa-save"></i></Button>

    <ModalDialog v-model="visible" :loading="loading" header="Save Query" @onSave="create">
        <Form>
            <Field label="Name">
                <Input v-model="model.name"></Input>
            </Field>
        </Form>
    </ModalDialog>
</template>
