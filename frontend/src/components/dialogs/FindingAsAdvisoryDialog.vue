<script>
import FindingService from '@/service/FindingService';
import TechnologySelectField from "@/components/elements/forms/TechnologySelectField.vue";

export default {
    name: 'FindingAsAdvisoryDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            loading: false,
            model: {
                technology: null,
                affected_versions: null
            },
            service: new FindingService()
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
            this.loading = true;
            let data = {
                technology: this.model.technology,
                affected_versions: this.model.affected_versions
            };
            this.service
                .findingAsAdvisory(this.$api, this.projectId, this.findingId, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Finding copies as advisory!',
                        life: 3000,
                        detail: 'Finding was successfully copied as advisory!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { TechnologySelectField }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Finding As Advisory" outlined @click="open"></Button>

    <Dialog header="Create Advisory from Finding" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="product">Product</label>
                <TechnologySelectField v-model="model.technology"></TechnologySelectField>
            </div>
            <div class="field col-12">
                <label for="versions">Affected Versions</label>
                <InputText v-model="model.affected_versions" id="versions"></InputText>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" :loading="loading" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>