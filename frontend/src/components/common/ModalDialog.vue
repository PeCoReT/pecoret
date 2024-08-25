<script>
export default {
    name: 'ModalDialog',
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
    <Dialog :header="header" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <slot></slot>
        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="this.$emit('onSave')" icon="pi pi-check" class="p-button-outlined" :loading="this.saveLoading"></Button>
        </template>
    </Dialog>
</template>
