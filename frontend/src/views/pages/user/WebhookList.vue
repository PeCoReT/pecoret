<script>
import UserSettingsPageLayout from '@/layout/UserSettingsPageLayout.vue';
import SearchField from '@/partials/common/SearchField.vue';
import { Button } from '@/components/ui/button';
import { DataViewContent, DataViewHeader } from '@/components/dataview';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'WebhookList',
    mixins: [listViewMixin],
    components: { DataViewHeader, SearchField, UserSettingsPageLayout, Button, DataViewContent },
    data() {
        return {
            items: [],
            loading: false,
            filters: {
                search: { value: null }
            }
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        confirmDialogDelete(item) {
            this.$confirm.require({
                message: 'Do you want to delete this item?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                accept: () => {
                    this.$api.delete(this.$api.e.webhookDetail, { pk: item.pk }).then(() => {
                        this.getItems();
                    });
                }
            });
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            this.$api
                .get(this.$api.e.webhookList, null, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    }
};
</script>

<template>
    <UserSettingsPageLayout subheadline="Connect applications to PeCoReT" headline="Webhook">
        <div class="py-6">
            <div class="col-span-12">
                <div class="flex justify-between items-center w-full">
                    <div class="flex-1 pr-2">
                        <SearchField v-model="filters.search.value" @search="onSearch"></SearchField>
                    </div>
                    <div class="flex-shrink-0">
                        <Button :href="this.$router.resolve({ name: 'WebhookCreate' }).href" as="a">
                            <i class="fa fa-plus"></i>
                            Webhook
                        </Button>
                    </div>
                </div>
            </div>
            <div class="py-4">
                <DataViewHeader :total-records="totalRecords"></DataViewHeader>
                <DataViewContent :items="items" :loading="loading" blank-slate-title="No Webhooks!"
                    blank-slate-icon="fa fa-plug" blank-slate-text="No webhooks found!">
                    <template #item="{ item }">
                        <div class="flex-1">[{{ item.provider }}] {{ item.url }}</div>
                        <Button variant="outline" as="a"
                            :href="this.$router.resolve({ name: 'WebhookUpdate', params: { webhookId: item.pk } }).href">
                            <i class="fa fa-edit"></i>
                            Edit
                        </Button>
                        <Button variant="destructive" @click="confirmDialogDelete(item)"><i class="fa fa-trash"></i>
                            Delete
                        </Button>
                    </template>
                </DataViewContent>
            </div>
        </div>
    </UserSettingsPageLayout>
</template>
