<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Paginator } from '@/components/paginator';
import { Button } from '@/components/ui/button';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import { listViewMixin } from "@/mixins/listViewMixin";

export default {
    name: 'ContributorList',
    mixins: [listViewMixin],
    data() {
        return {
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            selection: {},
            filters: {
                search: { value: null }
            }
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.pMembershipList, { projectPk: this.projectId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        async bulkDelete() {
            this.$confirm.require({
                accept: async () => {
                    let itemsDeleted = 0;
                    let totalLength = Object.entries(this.selection).length;
                    for (const [key, value] of Object.entries(this.selection)) {
                        itemsDeleted++;
                        if (value === true) {
                            await this.$api
                                .delete(this.$api.e.pMembershipDetail, {
                                    projectPk: this.projectId,
                                    pk: key
                                })
                                .then(() => {
                                    if (itemsDeleted === totalLength) {
                                        this.selection = {};
                                        this.getItems();
                                    }
                                });
                        }
                    }
                }
            });
        }
    },
    components: {
        DataViewHeader,
        Paginator,
        DataViewContent,
        SearchField,
        DataViewListLayout,
        Button
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #search>
            <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
        </template>
        <template #create-button>
            <Button
                :href="this.$router.resolve({ name: 'ContributorCreate', params: { projectId: this.projectId } }).href"
                as="a" variant="outline"><i class="fa fa-plus"></i> Contributor </Button>
        </template>

        <DataViewHeader v-model:items="items" :show-bulk-select="true" v-model:selection="selection"
            :total-records="totalRecords">
            <template #bulk>
                <Button @click="bulkDelete" variant="destructive">Delete</Button>
            </template>
        </DataViewHeader>

        <DataViewContent :items="items" :loading="loading" v-model:selection="selection" :show-bulk-select="true">
            <template #item="{ item }">
                <div class="flex-1">
                    {{ item.user.username }}
                    <div class="flex text-xs text-muted-foreground">
                        {{ item.role }}
                    </div>
                </div>
                <span class="text-sm text-muted-foreground">
                    {{ item.active_until || 'Never' }}
                </span>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords"
            class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
