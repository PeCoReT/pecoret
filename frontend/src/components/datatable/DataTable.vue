<script>
import { Table, TableHeader, TableBody, TableHead, TableRow, TableCell } from '@/components/ui/table';
import BlankSlate from '@/components/blankslate/BlankSlate.vue';
import DefaultSkeleton from '@/components/skeleton/DefaultSkeleton.vue';
import { Checkbox } from '@/components/ui/checkbox';
import { LoadingBar } from '@/components/loading';

export default {
    name: 'DataTable',
    components: {
        Table,
        TableHeader,
        TableBody,
        TableHead,
        TableRow,
        TableCell,
        BlankSlate,
        DefaultSkeleton,
        Checkbox,
        LoadingBar
    },
    props: {
        columns: { type: Array, required: true },
        items: { type: Array, required: true },
        loading: { type: Boolean, required: true },
        totalRecords: { type: Number, required: true },
        showBulkSelect: { type: Boolean, default: false },
        selection: { type: Object, default: () => ({}) },
        blankSlateIcon: String,
        blankSlateText: String,
        blankSlateTitle: String,
        skeletonRows: { type: Number, default: 3 }
    },
    emits: ['bulkSelect', 'update:selection'],
    data() {
        return { bulkSelect: false };
    },
    computed: {
        colSpan() {
            return this.columns.length + (this.showBulkSelect ? 1 : 0);
        },
        hasSelection() {
            return Object.values(this.selection).includes(true);
        }
    },
    methods: {
        onBulkToggle(checked) {
            this.bulkSelect = checked;
            const newSel = {};
            if (checked) {
                this.items.forEach((i) => {
                    newSel[i.pk] = true;
                });
            }
            this.$emit('update:selection', newSel);
            this.$emit('bulkSelect', checked);
        }
    },
    watch: {
        selection: {
            immediate: true,
            handler() {
                if (!this.hasSelection) this.bulkSelect = false;
            }
        }
    }
};
</script>

<template>
    <div>
        <!-- Header (filters, bulk actions, record count) -->
        <div class="bg-muted text-muted-foreground p-2 px-4 border rounded-t-lg shadow-sm mt-3">
            <div class="flex items-center">
                <div class="p-1 flex items-center">
                    <span>{{ totalRecords }} Items</span>
                </div>
                <div class="flex flex-1 justify-end">
                    <slot name="bulk" v-if="hasSelection" />
                    <slot name="filters" v-else />
                </div>
            </div>
        </div>

        <!-- Table -->
        <Table class="w-full border border-border table-fixed">
            <TableHeader>
                <!-- Checkbox header cell: fixed width, centered, no jump -->
                <TableHead v-if="showBulkSelect" class="border-b bg-accent p-0 text-center align-middle w-10" style="width: 2.5rem">
                    <div class="flex items-center justify-center h-11">
                        <Checkbox v-model:checked="bulkSelect" class="h-4 w-4" @update:checked="onBulkToggle" />
                    </div>
                </TableHead>

                <!-- Regular headers -->
                <TableHead v-for="col in columns" :key="col.key" class="border-b bg-accent p-2 px-4 align-middle">
                    {{ col.title }}
                </TableHead>
            </TableHeader>

            <TableBody>
                <!-- Loading row: spans all columns -->
                <template v-if="loading">
                    <TableRow>
                        <TableCell :colspan="colSpan" class="p-0 border-t-0">
                            <LoadingBar height="3px" />
                        </TableCell>
                    </TableRow>
                </template>

                <!-- Blank Slate -->
                <template v-else-if="!items.length">
                    <TableRow class="cursor-default hover:bg-transparent">
                        <TableCell :colspan="colSpan" class="p-0">
                            <slot name="blankslate">
                                <BlankSlate :icon="blankSlateIcon" :text="blankSlateText" :title="blankSlateTitle" class="border rounded-t-none rounded-b-lg" />
                            </slot>
                        </TableCell>
                    </TableRow>
                </template>

                <!-- Data Rows -->
                <template v-else>
                    <TableRow v-for="(item, idx) in items" :key="item.pk" :class="[{ 'rounded-b-lg': idx === items.length - 1 }]" class="align-middle">
                        <!-- Checkbox cell: fixed width, centered, stable height -->
                        <TableCell v-if="showBulkSelect" class="p-0 text-center align-middle w-10" style="width: 2.5rem">
                            <div class="flex items-center justify-center h-11">
                                <Checkbox v-model:checked="selection[item.pk]" class="h-4 w-4" />
                            </div>
                        </TableCell>

                        <TableCell v-for="col in columns" :key="col.key" class="p-2 px-4 align-middle">
                            <slot name="cell" :item="item" :col="col">
                                {{ item[col.key] }}
                            </slot>
                        </TableCell>
                    </TableRow>
                </template>
            </TableBody>
        </Table>
    </div>
</template>
