<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import SortListDropdownMenu from '@/components/dropdown-menu/SortListDropdownMenu.vue';
import { commonSortFilter } from '@/utils/constants';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'ReportList',
    mixins: [listViewMixin],
    data() {
        return {
            projectId: this.$route.params.projectId,
            items: [],
            filters: {
                search: { value: null }
            },
            loading: false,
            showCreateForm: false,
            newReport: {
                name: null,
                template: null
            }
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        commonSortFilter() {
            return commonSortFilter;
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pReportList, { pPk: this.projectId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        create() {
            this.$api
                .post(this.$api.e.pReportList, { pPk: this.projectId }, this.newReport)
                .then(() => {
                    this.$toaster({
                        title: 'Report created!',
                        duration: 3000,
                        description: 'New report created!'
                    });
                    this.showCreateForm = false;
                    this.getItems();
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {
        Paginator,
        ModelCombobox,
        Label,
        Button,
        Input,
        DataViewContent,
        SortListDropdownMenu,
        DataViewHeader,
        SearchField,
        DataViewListLayout
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #create-button>
            <Button @click="
                () => {
                    this.showCreateForm = true;
                }
            ">
                <i class="fa fa-plus"></i> Report
            </Button>
        </template>

        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>

        <Card v-if="showCreateForm" class="col-span-12 mt-3">
            <div class="flex flex-wrap md:flex-nowrap items-stretch gap-4">
                <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                    <Label class="text-sm font-medium" for="name">Name</Label>
                    <Input id="name" v-model="newReport.name"></Input>
                </div>
                <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                    <Label class="text-sm font-medium">Report Template</Label>
                    <ModelCombobox v-model="newReport.template" :api-endpoint="this.$api.e.reportTemplateList"
                        label="Report Template" value-field="name">
                        <template #trigger="{ label }">
                            <Button class="justify-between" role="combobox" variant="outline">
                                {{ newReport.template ? label : 'Select template...' }}
                                <i class="ml-2 h-4 w-4 shrink-0 opacity-50 fa fa-chevron-down" />
                            </Button>
                        </template>
                    </ModelCombobox>
                </div>
                <div class="flex gap-2 ml-auto flex-col md:flex-row items-end mt-4 md:mt-0">
                    <Button variant="outline" @click="
                        () => {
                            this.showCreateForm = false;
                        }
                    ">Cancel
                    </Button>
                    <Button variant="default" @click="create">Save</Button>
                </div>
            </div>
        </Card>

        <DataViewHeader :total-records="totalRecords">
            <template #filters>
                <SortListDropdownMenu :items="commonSortFilter()"></SortListDropdownMenu>
            </template>
        </DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-file"
            blank-slate-text="No reports found!" blank-slate-title="No Reports!">
            <template #item="{ item }">
                <div class="flex-1">
                    <a :href="this.$router.resolve({ name: 'ReportDetail', params: { projectId: this.projectId, reportId: item.pk } }).href"
                        class="hover:underline">{{ item.name }}</a>

                    <div class="flex text-xs text-muted-foreground">
                        <span>Created: {{ item.date_created }}</span>
                        <span class="mx-2">|</span>
                        <span>Updated: {{ item.date_updated }}</span>
                    </div>
                </div>
                <span>{{ item.template }}</span>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
