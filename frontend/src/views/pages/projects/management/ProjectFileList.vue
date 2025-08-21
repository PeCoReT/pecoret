<script>
import forceFileDownload from '@/utils/file';
import DataViewListLayout from '@/layouts/DataViewListLayout.vue';
import DataViewContent from '@/components/dataview/DataViewContent.vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Paginator } from '@/components/paginator';
import DataViewHeader from '@/components/dataview/DataViewHeader.vue';
import { listViewMixin } from '@/mixins/listViewMixin';

export default {
    name: 'ProjectFileList',
    mixins: [listViewMixin],
    components: {
        DataViewHeader,
        Paginator,
        Label,
        Input,
        Button,
        DataViewContent,
        DataViewListLayout
    },
    data() {
        return {
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            filters: {},
            showCreateForm: false,
            newFile: {
                name: null,
                file: null
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
                .get(this.$api.e.pFileList, { pPk: this.projectId }, data)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        downloadFile(file_id) {
            this.$api
                .get(
                    this.$api.e.pFileDownload,
                    {
                        pPk: this.projectId,
                        pk: file_id
                    },
                    null,
                    { responseType: 'arraybuffer' }
                )
                .then((response) => {
                    forceFileDownload(response);
                });
        },
        create() {
            let formData = new FormData();
            formData.append('name', this.newFile.name);
            formData.append('file', this.newFile.file);
            this.$api.post(this.$api.e.pFileList, { pPk: this.projectId }, formData).then((response) => {
                this.$toaster({
                    title: 'File added!',
                    duration: 3000,
                    description: 'New file was added!'
                });
                this.showCreateForm = false;
                this.newFile.file = null;
                this.newFile.name = null;
                this.getItems();
            });
        },
        onFileUpload(event) {
            this.newFile.file = event.target.files[0];
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Dou you want to delete this file?',
                accept: () => {
                    this.$api.delete(this.$api.e.pFileDetail, { pPk: this.projectId, pk: id }).then(() => {
                        this.getItems();
                    });
                }
            });
        }
    }
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
            >
                <i class="fa fa-plus"></i> File
            </Button>
        </template>

        <div v-if="this.showCreateForm === true" class="flex flex-wrap md:flex-nowrap items-stretch gap-4 mt-3">
            <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                <Label class="text-sm font-medium" for="name">Name</Label>
                <Input id="name" v-model="newFile.name"></Input>
            </div>
            <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                <Label class="text-sm font-medium" for="file">File</Label>
                <Input type="file" @change="onFileUpload"></Input>
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
        <DataViewContent :items="items" :loading="loading" blank-slate-icon="fa fa-file" blank-slate-text="No project files found!" blank-slate-title="No Project Files!">
            <template #item="{ item }">
                <div class="flex-1">
                    {{ item.name }}
                    <div class="text-xs flex text-muted-foreground">
                        <span>Created: {{ item.date_created }}</span>
                    </div>
                </div>
                <Button variant="outline" @click="downloadFile(item.pk)">
                    <i class="fa fa-download" />
                </Button>
            </template>
        </DataViewContent>
        <Paginator :rows="this.pagination.limit" :total-records="this.totalRecords" class="w-full mt-3 flex justify-center" @page="onPage"></Paginator>
    </DataViewListLayout>
</template>
