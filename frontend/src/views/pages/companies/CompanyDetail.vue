<script>
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import CompanyUpdateDialog from '@/components/dialogs/CompanyUpdateDialog.vue';
import CompanyTabMenu from '@/components/navigation/CompanyTabMenu.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import markdown from '@/utils/markdown';
import CommendCard from '@/components/common/CommentCard.vue';
import { useAuthStore } from '@/store/auth';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

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
            this.$api.get(this.$api.e.cInfoList, { cPk: this.companyId }).then((response) => {
                this.companyInformation = response.data.results;
            });
        },
        companyInformationUpdated(information) {
            let data = { text: information.text };
            this.$api.patch(this.$api.e.cInfoDetail, { cPk: this.companyId, pk: information.pk }, data).then(() => {
                this.getCompanyInformation();
            });
        }
    },
    mounted() {
        this.getCompany();
        this.getCompanyInformation();
    },
    components: {
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
    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid grid-cols-12 mt-3">
        <div class="col-span-6">
            <div class="flex justify-start">
                <strong class="text-lg">{{ company.name }}</strong>
            </div>
        </div>
        <div class="col-span-6">
            <div class="flex justify-end">
                <CompanyUpdateDialog :company="company" @object-updated="getCompany"></CompanyUpdateDialog>
                <Button @click="confirmDialogDeleteCompany" outlined severity="danger" icon="fa fa-trash" label="Delete"></Button>
            </div>
        </div>
    </div>

    <div class="grid mt-3 grid-cols-12">
        <div class="col-span-12">
            <CompanyTabMenu></CompanyTabMenu>
            <div class="card border-noround-top">
                <div class="grid grid-cols-12 gap-3">
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Street" icon="fa-road" class="bg-surface-950" :text="company.street"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="City" icon="fa-city" class="bg-surface-950" :text="company.city"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Country" icon="fa-earth" class="bg-surface-950" :text="company.country"></DetailCardWithIcon>
                    </div>
                    <div class="col-span-12 md:col-span-3">
                        <DetailCardWithIcon title="Report Template" icon="fa-file" class="bg-surface-950" :text="company.report_template"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid grid-cols-12 mt-3">
                    <div class="col-span-12">
                        <p class="text-xl">Company Information</p>
                        <Form class="mb-3">
                            <Field>
                                <MarkdownEditor max-height="200px" v-model="newInformationText"></MarkdownEditor>
                            </Field>
                            <Button class="w-full" label="Save" @click="createCompanyInformation"></Button>
                        </Form>
                        <div class="text-base pt-2 pb-2" v-for="info in companyInformation" :key="info.pk">
                            <CommendCard :comment="info" @onDelete="confirmDialogDelete" @on-edit="companyInformationUpdated"></CommendCard>
                        </div>

                        <BlankSlate v-if="companyInformation.length < 1" icon="fa fa-circle-info" text="No company information found!" title="No company information!"></BlankSlate>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
