<script>
import { Checkbox } from '@/components/ui/checkbox';

export default {
    name: 'DataViewHeader',
    components: { Checkbox },
    props: {
        totalRecords: {
            required: true
        },
        showBulkSelect: {
            default: false
        },
        selection: {
            required: false,
            default: {}
        },
        items: {
            required: false
        }
    },
    emit: ['bulkSelect', 'update:selection'],
    data() {
        return {
            bulkSelect: false,
            selectedItems: this.selection || {}
        };
    },
    methods: {
        onBulkSelect(event) {
            this.$emit('update:bulkCheckbox', event);
            this.$emit('bulkSelect', this.bulkSelect);
            if (event === true) {
                for (let i = 0; i < this.items.length; i++) {
                    this.selectedItems[this.items[i].pk] = true;
                }
            } else {
                this.selectedItems = {};
                this.bulkSelect = false;
            }
            this.$emit('update:selection', this.selectedItems)
        }
    },
    computed: {
        hasBulkSelectedItem() {
            if (!this.selection) {
                return false;
            }
            return Object.values(this.selection).includes(true);
        }
    },
    watch: {
        selection: {
            immediate: true,
            handler(value) {
                if (!this.hasBulkSelectedItem) {
                    this.bulkSelect = false
                }
            }
        }
    }
};
</script>

<template>
    <div class="bg-muted text-muted-foreground p-2 px-4 border rounded-t-lg shadow-sm mt-3">
        <div class="flex items-center">
            <div class="flex justify-start">
                <div class="flex items-center">
                    <span v-if="showBulkSelect === true" class="flex items-center">
                        <Checkbox v-model:checked="bulkSelect" class="mr-3" @update:checked="onBulkSelect"></Checkbox>
                    </span>
                    <span>{{ totalRecords }} Items</span>
                </div>
            </div>
            <div class="flex flex-1 justify-end">
                <span v-if="hasBulkSelectedItem" class="flex items-center gap-2"> <slot name="bulk"></slot> </span>
                <span v-else> <slot name="filters"></slot> </span>
            </div>
        </div>
    </div>
</template>
