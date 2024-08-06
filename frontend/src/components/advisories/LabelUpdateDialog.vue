<script>
import AdvisoryService from "@/service/AdvisoryService";


export default {
  name: "LabelUpdateDialog",
  emits: ["object-updated"],
  props: {
    label: {
      required: true
    }
  },
  data() {
    return {
      visible: false,
      model: {
        name: this.label.name,
        description: this.label.description,
        color: this.label.color
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
    patch() {
      if (this.model.color.startsWith("#") === false) {
        this.model.color = "#" + this.model.color;
      }
      let data = {
        name: this.model.name,
        description: this.model.description,
        color: this.model.color
      };

      this.service.patchLabel(this.label.pk, data).then((response) => {
        this.$emit("object-updated", response.data);
        this.visible = false;
      });
    }
  },
  watch: {
    label: {
      immediate: true,
      deep: true,
      handler(value) {
        this.model = value;
      }
    }
  }
};
</script>

<template>
  <Button icon="fa fa-pen-to-square" size="small" outlined @click="open"></Button>

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
      <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
    </template>
  </Dialog>
</template>