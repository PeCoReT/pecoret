<script>
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import {Button} from '@/components/ui/button';

export default {
    name: 'ModalDialog',
    components: {
        Button,
        Dialog,
        DialogContent,
        DialogDescription,
        DialogFooter,
        DialogHeader,
        DialogTitle,
        DialogTrigger
    },
    props: {
        modelValue: {
            required: true,
            default: false
        },
        header: {
            required: true
        },
        loading: {
            required: true
        }
    },
    emit: ['update:modelValue', 'onSave'],
    data() {
        return {
            visible: this.modelValue,
            saveLoading: this.loading
        };
    },
    methods: {
        close() {
            this.visible = false;
            this.$emit('update:modelValue', false);
        }
    },
    watch: {
        modelValue(value) {
            this.visible = value;
        },
        loading(value) {
            this.saveLoading = value;
        }
    }
};
</script>

<template>
    <Dialog v-model:open="visible">
        <DialogTrigger>
            <slot name="trigger"></slot>
        </DialogTrigger>
        <DialogContent>
            <DialogDescription></DialogDescription>
            <DialogHeader>
                <DialogTitle>{{ header }}</DialogTitle>
            </DialogHeader>
            <slot></slot>

            <DialogFooter>
                <Button variant="outline" @click="close">Cancel</Button>
                <Button @click="this.$emit('onSave')">
                    <i class="fa fa-check"/> Save
                </Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>
