<script>
import AdvisoryService from '@/service/AdvisoryService';
import ModalDialog from '@/components/elements/dialogs/ModalDialog.vue';

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
                .createTimeline(this.$api, this.advisoryId, data)
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
        <div class="p-fluid grid formgrid">
            <div class="field col-12">
                <label for="text">Text</label>
                <InputText id="text" v-model="model.text"></InputText>
            </div>
            <div class="field col-12">
                <label for="date">Date</label>
                <Calendar v-model="model.date" id="date"></Calendar>
            </div>
        </div>
    </ModalDialog>
</template>
