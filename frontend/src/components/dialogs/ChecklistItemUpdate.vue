<script>
import ChecklistService from "@/service/ChecklistService";
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ChecklistItemUpdate',
    props: {
        item: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.command,
            service: new ChecklistService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        patch() {
            let data = {
                description: this.model.description,
                name: this.model.name,
                item_id: this.model.item_id
            };
            this.service.patchItem(this.$api, this.item.pk, data).then(() => {
                this.$emit('object-updated', this.model);
                this.visible = false;
            });
        }
    },
    watch: {
        item: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    components: { MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <Dialog header="Update Item" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="id">Item ID</label>
                <InputText id="id" type="text" v-model="model.item_id"></InputText>
            </div>
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </div>
            <div class="field col-12">
                <label for="output">Description</label>
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>