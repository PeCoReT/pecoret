<script>
import { ModalDialog } from '@/components/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {DatePicker} from '@/components/datepicker';

export default {
    name: 'ShareTokenCreateDialog',
    components: { ModalDialog, Button, Input, DatePicker },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            model: {
                name: null,
                date_expire: null
            },
            loading: false,
            advisoryId: this.$route.params.advisoryId
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        create() {
            this.$api.post(this.$api.e.aShareTokenList, { aPk: this.advisoryId }, this.model).then(() => {
                this.$toaster({
                    title: 'Token created!',
                    duration: 3000,
                    description: 'Token created successfully!'
                });
                this.$emit('object-created');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button @click="open"> <i class="fa fa-plus"></i> Share Token </Button>
    <ModalDialog v-model="showDialog" v-model:loading="loading" header="New Share Token" @onSave="create">
        <Form>
            <Field label="Name">
                <Input v-model="model.name"></Input>
            </Field>
            <Field label="Date Expire?">
                <DatePicker v-model="model.date_expire"></DatePicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
