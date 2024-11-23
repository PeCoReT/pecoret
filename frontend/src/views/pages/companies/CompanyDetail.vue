<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import CompanyUpdateDialog from '@/components/dialogs/CompanyUpdateDialog.vue';
import CompanyTabMenu from '@/components/navigation/CompanyTabMenu.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import markdown from '@/utils/markdown';
import CommendCard from '@/components/common/CommentCard.vue';
import { useAuthStore } from '@/store/auth';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import BaseLayout from '@/layout/base/BaseLayout.vue';

export default {
    name: 'CompanyDetail',
    data() {
        return {
            companyId: this.$route.params.companyId,
            breadcrumbs: [
                { label: 'Companies', to: this.$router.resolve({ name: 'CompanyList' }) },
                { label: 'Company Detail', disabled: true }
            ],
            company: { report_template: {} },
            authStore: useAuthStore(),
            companyInformation: [],
            pagination: { limit: 25, page: 1 },
            totalRecords: 0,
            logoUrl: null,
            newInformationText: null
        };
    },
    methods: {
        renderMarkdown(text) {
            return markdown.renderMarkdown(text);
        },
        getCompany() {
            this.$api.get(this.$api.e.companyDetail, { pk: this.companyId }).then((response) => {
                this.company = response.data;
                if (this.company.has_logo === true) {
                    this.logoUrl = `/api/companies/${this.companyId}/logo/`;
                }
            });
        },
        createCompanyInformation() {
            this.$api.post(this.$api.e.cInfoList, { cPk: this.companyId }, { text: this.newInformationText }).then(() => {
                this.newInformationText = null;
                this.getCompanyInformation();
            });
        },
        confirmDialogDelete(comment) {
            let id = comment.pk;
            this.$confirm.require({
                message: 'Do you want to delete this item?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.cInfoDetail, { cPk: this.companyId, pk: id }).then(() => {
                        this.getCompanyInformation();
                    });
                }
            });
        },
        confirmDialogDeleteCompany() {
            this.$confirm.require({
                message: 'Do you want to delete this item? This will remove all projects related to the company!',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.$api.delete(this.$api.e.companyDetail, { pk: this.companyId }).then(() => {
                        this.$router.push({ name: 'CompanyList' });
                    });
                }
            });
        },
        getCompanyInformation() {
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.$api.get(this.$api.e.cInfoList, { cPk: this.companyId }, params).then((response) => {
                this.companyInformation = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        companyInformationUpdated(information) {
            let data = { text: information.text };
            this.$api.patch(this.$api.e.cInfoDetail, { cPk: this.companyId, pk: information.pk }, data).then(() => {
                this.getCompanyInformation();
            });
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getCompanyInformation();
        }
    },
    mounted() {
        this.getCompany();
        this.getCompanyInformation();
    },
    components: {
        BaseLayout,
        MarkdownEditor,
        DetailCardWithIcon,
        CompanyUpdateDialog,
        CompanyTabMenu,
        BlankSlate,
        CommendCard
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <div class="card col-span-12">
            <div class="flex justify-between items-center">
                <div class="flex items-center space-x-4">
                    <div class="w-24 h-24 bg-gray-700 flex items-center justify-center rounded-full" v-if="!this.company.has_logo">
                        <span class="text-sm text-gray-500">Logo</span>
                    </div>
                    <div class="w-24 h-24 flex items-center justify-center rounded-full" v-else>
                        <img :src="this.logoUrl" />
                    </div>
                    <div>
                        <h1 class="text-2xl font-bold text-gray-100">{{ company.name }}</h1>
                        <p class="text-gray-400">{{ company.street }}, {{ company.city }}, {{ company.country }}</p>
                    </div>
                </div>
                <div class="flex space-x-4">
                    <CompanyUpdateDialog :company="company" @object-updated="getCompany"></CompanyUpdateDialog>
                    <Button @click="confirmDialogDeleteCompany" outlined severity="danger" icon="fa fa-trash" label="Delete"></Button>
                </div>
            </div>
            <div class="mt-4">
                <h2 class="text-lg font-semibold text-gray-200">Report Template:</h2>
                <p class="text-gray-400">{{ company.report_template }}</p>
            </div>
        </div>

        <div class="col-span-12">
            <CompanyTabMenu></CompanyTabMenu>
            <div class="card">
                <Form class="mb-3">
                    <Field label="New Information">
                        <MarkdownEditor max-height="200px" v-model="newInformationText"></MarkdownEditor>
                    </Field>
                    <Button class="w-full" label="Save" @click="createCompanyInformation"></Button>
                </Form>
                <div class="text-base pt-2 pb-2" v-for="info in companyInformation" :key="info.pk">
                    <CommendCard :comment="info" @onDelete="confirmDialogDelete" @on-edit="companyInformationUpdated"></CommendCard>
                </div>
                <Paginator :rows="pagination.limit" :totalRecords="totalRecords" @page="onPage"></Paginator>

                <BlankSlate v-if="companyInformation.length < 1" icon="fa fa-circle-info" text="No company information found!" title="No company information!"></BlankSlate>
            </div>
        </div>
    </BaseLayout>
</template>
