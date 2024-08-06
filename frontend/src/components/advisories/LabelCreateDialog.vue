<script>
import AdvisoryService from '@/service/AdvisoryService'


export default {
  name: "LabelCreateDialog",
  emits: ["object-created"],
  data() {
    return {
      visible: false,
      model: {
        name: null,
        description: null,
        color: null
      },
      service: new AdvisoryService()
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
      }
      this.service.createLabel(data).then((response) => {
        this.$toast.add({
          severity: "success",
          summary: "Label created!",
          life: 3000,
          detail: "New label was created successfully!"
        });
        this.$emit("object-created", response.data);
        this.visible = false;
      });
    }
  },
}
</script>

<template>
  <Button icon="fa fa-plus" label="Label" outlined @click="open"></Button>

  <Dialog header="Create Label" v-model:visible="visible" modal :style="{ width: '70vw' }">
    <div class="p-fluid formgrid grid">
      <div class="field col-12">
        <label for="name">Name</label>
        <InputText id="name" v-model="model.name"></InputText>
      </div>
      <div class="field col-12">
        <label for="description">Description</label>
        <InputText id="description" maxlength="254" v-model="model.description"></InputText>
      </div>
      <div class="field col-12">
        <label for="color" class="mr-3">Color</label>
        <ColorPicker v-model="model.color"></ColorPicker>
      </div>
    </div>


    <template #footer>
      <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
      <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
    </template>
  </Dialog>
</template>