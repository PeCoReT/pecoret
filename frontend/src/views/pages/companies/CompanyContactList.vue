<script>
import { BlankSlate } from '@/components/blankslate';
import { CompanyTabMenu } from '@/partials/companies';
import { Button } from '@/components/ui/button';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import SearchField from '@/partials/common/SearchField.vue';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'CompanyContactList',
    mixins: [listViewMixin],
    data() {
        return {
            items: [],
            loading: false,
            filters: {
                search: { value: null }
            },
            selection: {},
            companyId: this.$route.params.companyId
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        async bulkDeleteCallback(key, value) {
            return this.$api.delete(this.$api.e.cContactDetail, { pk: key, cPk: this.companyId });
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.cContactList, { cPk: this.companyId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        search(query) {
            this.getItems({ search: query });
        }
    },
    components: {
        SearchField,
        DataViewContent,
        DataViewHeader,
        DataViewListLayout,
        BlankSlate,
        CompanyTabMenu,
        Button
    }
};
</script>

<template>
    <DataViewListLayout>
        <template #pre-content>
            <div class="mt-3">
                <CompanyTabMenu></CompanyTabMenu>
            </div>
        </template>

        <template #search>
            <SearchField v-model="filters.search.value" @search="search"></SearchField>
        </template>
        <template #create-button>
            <Button :href="this.$router.resolve({ name: 'CompanyContactCreate', params: { companyId: this.companyId } }).href" as="a"><i class="fa fa-plus"></i> Contact </Button>
        </template>
        <DataViewHeader :total-records="totalRecords" v-model:selection="selection" v-model:items="items" :show-bulk-select="true">
            <template #filters></template>
            <template #bulk>
                <Button @click="bulkDelete(this.bulkDeleteCallback)" variant="destructive">Delete</Button>
            </template>
        </DataViewHeader>
        <DataViewContent :show-bulk-select="true" v-model:selection="selection" :items="items" :loading="loading" blank-slate-icon="fa fa-address-card" blank-slate-text="No contacts found!" blank-slate-title="No Contacts!">
            <template #item="{ item }">
                <div class="flex-1">
                    <a :href="this.$router.resolve({ name: 'CompanyContactUpdate', params: { companyId: this.companyId, contactId: item.pk } }).href" class="hover:underline">{{ item.first_name }} {{ item.last_name }}</a>
                    <div class="flex text-muted-foreground text-sm">Email: {{ item.email }}</div>
                    <div class="flex text-muted-foreground text-sm">
                        <span>Phone: {{ item.phone || '-' }}</span>
                    </div>
                </div>
                <div class="flex">
                    <span>Role: {{ item.role }}</span>
                </div>
            </template>
        </DataViewContent>
    </DataViewListLayout>
</template>
