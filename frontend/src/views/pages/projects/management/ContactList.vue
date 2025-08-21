<script>
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Button } from '@/components/ui/button';
import ModelCombobox from '@/components/combobox/ModelCombobox.vue';
import { Label } from '@/components/ui/label';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import { Paginator } from '@/components/paginator';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'ContactList',
    mixins: [listViewMixin],
    data() {
        return {
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            newContact: { contact: null },
            showCreateForm: false,
            project: { company: {} },
            filters: {}
        };
    },
    mounted() {
        this.$api.get(this.$api.e.projectDetail, { pk: this.projectId }).then((response) => {
            this.project = response.data;
            this.getItems();
        });
    },
    methods: {
        create() {
            this.$api.post(this.$api.e.projectsContactList, { projectPk: this.projectId }, this.newContact).then(() => {
                this.$toaster({
                    title: 'Contact added!',
                    duration: 3000,
                    description: 'Contact added to project!'
                });
                this.showCreateForm = false;
                this.getItems();
            });
        },
        getItems(params) {
            this.loading = true;
            let data = this.buildParams(this.pagination, this.filters, params);
            let url = this.$api.e.projectsContactList;
            this.$api
                .get(url, { projectPk: this.projectId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(contactId) {
            this.$confirm.require({
                message: 'Do you want to delete this contact?',
                accept: () => {
                    this.deleteContact(contactId);
                }
            });
        },
        deleteContact(contactId) {
            this.$api.delete(this.$api.e.projectsContactDetail, { projectPk: this.projectId, pk: contactId }).then(() => {
                this.$toaster({
                    title: 'Contact Removed!',
                    description: 'Removed contact from project!',
                    duration: 3000
                });
                this.getItems();
            });
        }
    },
    components: { Paginator, DataViewHeader, Label, ModelCombobox, DataViewContent, DataViewListLayout, Button }
};
</script>

<template>
    <DataViewListLayout>
        <template #create-button>
            <Button
                @click="
                    () => {
                        this.showCreateForm = true;
                    }
                "
                ><i class="fa fa-plus"></i> Contact
            </Button>
        </template>

        <div v-if="showCreateForm === true" class="card flex flex-wrap md:flex-nowrap items-stretch gap-4 mt-3">
            <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                <Label class="text-sm font-medium">Contact</Label>
                <ModelCombobox v-model="newContact.contact" :api-endpoint="this.$api.e.cContactList" :url-args="{ cPk: project.company.pk }" label-field="last_name" value-field="pk" variant="form"></ModelCombobox>
            </div>
            <div class="flex gap-2 ml-auto flex-col md:flex-row items-end mt-4 md:mt-0">
                <Button
                    variant="outline"
                    @click="
                        () => {
                            this.showCreateForm = false;
                        }
                    "
                    >Cancel
                </Button>
                <Button variant="default" @click="create">Save</Button>
            </div>
        </div>

        <DataViewHeader :total-records="totalRecords"></DataViewHeader>
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-id-card" blank-slate-text="No contacts found!" blank-slate-title="No Contacts!">
            <template #item="{ item }">
                <div class="flex-1">
                    {{ item.contact.first_name }} {{ item.contact.last_name }}
                    <div class="flex text-muted-foreground text-sm">Email: {{ item.contact.email }}</div>
                    <div class="flex text-muted-foreground text-sm">
                        <span>Phone: {{ item.contact.phone || '-' }}</span>
                    </div>
                </div>
                <div class="flex">
                    <span>Role: {{ item.contact.role }}</span>
                </div>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
