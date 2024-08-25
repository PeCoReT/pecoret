<script>
import AdvisoryService from '@/service/AdvisoryService';
import ModalDialog from '@/components/common/ModalDialog.vue';

export default {
    name: 'AdvisoryTimelineCreateDialog',
    components: { ModalDialog },
    emits: ['object-created'],
    data() {
        return {
            showDialog: false,
            advisoryId: this.$route.params.advisoryId,
            model: {
                text: null,
                date: null
            },
            loading: false,
            service: new AdvisoryService()
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
            this.service
                .createTimeline(this.advisoryId, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Timeline added!',
                        life: 3000,
                        detail: 'Timeline added to Advisory!'
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

    <ModalDialog :loading="loading" header="Create Timeline Entry" v-model="showDialog" @onSave="create">
        <Form>
            <Field label="Text">
                <InputText v-model="model.text"></InputText>
            </Field>
            <Field label="Date">
                <DatePicker v-model="model.date"></DatePicker>
            </Field>
        </Form>
    </ModalDialog>
</template>
