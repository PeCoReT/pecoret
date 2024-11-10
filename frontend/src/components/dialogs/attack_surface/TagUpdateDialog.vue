<script>
import ModalDialog from '@/components/common/ModalDialog.vue';

export default {
    name: 'TagUpdateDialog',
    components: { ModalDialog },
    emits: ['object-updated'],
    props: {
        tag: {
            required: true
        }
    },
    data() {
        return {
            showDialog: false,
            model: this.tag,
            loading: false,
        };
    },
    methods: {
        open() {
            this.showDialog = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                description: this.model.description,
                color: this.model.color
            };
            if (this.model.color.substring(0, 1) !== '#') {
                data = `#${this.model.color}`;
            }
            this.$api.patch(this.$api.e.asTagDetail, {pk: this.tag.pk}, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Tag updated!',
                    life: 3000,
                    detail: 'Tag updated successfully'
                });
                this.$emit('object-updated');
                this.showDialog = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-edit" size="small" outlined @click="open"></Button>

    <ModalDialog v-model:loading="loading" header="Update Tag" v-model="showDialog" @onSave="patch">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name" id="name"></InputText>
            </Field>
            <Field label="Description">
                <InputText id="description" maxlength="254" v-model="model.description"></InputText>
            </Field>
            <Field label="Color">
                <ColorPicker v-model="model.color"></ColorPicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
