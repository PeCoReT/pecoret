<script>

export default {
    name: 'LabelCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            model: {
                name: null,
                description: null,
                color: null
            },
            loading: false,
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
                name: this.model.name,
                description: this.model.description,
                color: '#' + this.model.color
            };
            this.$api.post(this.$api.e.aLabelList, null, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Label created!',
                    life: 3000,
                    detail: 'New label was created successfully!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Label" outlined @click="open"></Button>
    <ModalDialog header="Create Label" v-model="visible" :loading="loading" @onSave="create">
        <Form>
            <Field label="Name">
                <InputText v-model="model.name"></InputText>
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
