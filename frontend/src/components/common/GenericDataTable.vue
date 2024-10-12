<script>
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'GenericDataTable',
    components: { BlankSlate },
    emits: ['rowClick', 'page', 'filter', 'sort', 'update:selection', 'update:filters', 'update:modelValue', 'search', 'refresh'],
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
            required: false,
            default: 'menu'
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
        },
        showRefreshButton: {
            required: false,
            default: false
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
        },
        onRefresh() {
            this.$emit('refresh');
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
                <div class="flex flex-row">
                    <div class="flex-none pl-0">
                        <div v-if="showSearch === true">
                            <IconField iconPosition="left">
                                <InputIcon class="fa fa-search"></InputIcon>
                                <InputText @update:modelValue="onSearch" placeholder="Keyword Search" style="width: 100%" />
                            </IconField>
                        </div>
                    </div>
                    <div class="flex-none my-auto min-h-max">
                        <slot name="bulk-edit"></slot>
                    </div>

                    <span class="flex-grow"></span>
                    <div v-if="showRefreshButton === true" class="justify-end flex pr-0">
                        <Button @click="onRefresh" icon="fa fa-refresh" rounded outlined severity="secondary"></Button>
                    </div>
                    <slot name="header-right"></slot>
                </div>
            </slot>
        </template>
        <slot></slot>
        <template #footer>
            Total {{totalRecords}} items.
        </template>
    </DataTable>
</template>
