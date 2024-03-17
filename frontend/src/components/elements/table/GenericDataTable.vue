<script>
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'GenericDataTable',
    components: { BlankSlate },
    emits: ['rowClick', 'page', 'filter', 'sort', 'update:selection', 'update:filters', 'update:modelValue', 'search'],
    props: {
        modelValue: {
            required: true
        },
        blankSlateIcon: {
            required: true
        },
        blankSlateTitle: {
            required: true
        },
        blankSlateText: {
            required: true
        },
        pagination: {
            required: true
        },
        loading: {
            required: true
        },
        totalRecords: {
            required: true
        },
        filters: {
            required: false
        },
        filter: {
            type: Boolean,
            default: false,
            required: false
        },
        filterDisplay: {
            required: false
        },
        selection: {
            required: false,
            default: null
        },
        showSearch: {
            required: false,
            default: false
        },
        removableSort: {
            required: false
        }
    },
    data() {
        return {
            items: this.modelValue,
            filterModel: this.filters,
            selectedItems: this.selection
        };
    },
    methods: {
        rowClick(row) {
            this.$emit('rowClick', row);
        },
        onPage(event) {
            this.$emit('page', event);
        },
        onFilter(event) {
            this.$emit('filter', event);
        },
        onSort(event) {
            this.$emit('sort', event);
        },
        onUpdateSelection() {
            this.$emit('update:selection', this.selectedItems);
        },
        onUpdateFilters() {
            this.$emit('update:filters', this.filterModel);
        },
        onSearch(data) {
            this.$emit('search', data);
        }
    },
    watch: {
        modelValue: {
            deep: true,
            immediate: true,
            handler(value) {
                this.items = value;
            }
        },
        filters: {
            deep: true,
            immediate: true,
            handler(value) {
                this.filterModel = value;
            }
        },
        selection: {
            deep: true,
            immediate: true,
            handler(value) {
                this.selectedItems = value;
            }
        }
    }
};
</script>

<template>
    <DataTable
        @row-click="rowClick"
        :paginator="true"
        dataKey="pk"
        :rowHover="this.items.length > 0"
        :rows="pagination.limit"
        :value="items"
        :lazy="true"
        :totalRecords="totalRecords"
        :loading="loading"
        @page="onPage"
        @filter="onFilter"
        @sort="onSort"
        :removable-sort="removableSort"
        :filter="filter"
        :filterDisplay="filterDisplay"
        v-model:filters="filterModel"
        v-model:selection="selectedItems"
        @update:filters="onUpdateFilters"
        @update:selection="onUpdateSelection"
    >
        <template #empty>
            <slot name="empty">
                <BlankSlate :title="blankSlateTitle" :icon="blankSlateIcon" :text="blankSlateText"></BlankSlate>
            </slot>
        </template>
        <template #header>
            <slot name="header">
                <div class="grid" v-if="showSearch === true">
                    <IconField iconPosition="left">
                        <InputIcon class="fa fa-search"></InputIcon>
                        <InputText @update:modelValue="onSearch" placeholder="Keyword Search" style="width: 100%" />
                    </IconField>
                </div>
            </slot>
        </template>
        <slot></slot>
    </DataTable>
</template>
