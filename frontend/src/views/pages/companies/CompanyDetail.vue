<script>
import CompanyService from '@/service/CompanyService';
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import CompanyInformationCreateDialog from '@/components/dialogs/CompanyInformationCreateDialog.vue';
import CompanyUpdateDialog from '@/components/dialogs/CompanyUpdateDialog.vue';
import CompanyTabMenu from '../../../components/pages/CompanyTabMenu.vue';
import BlankSlate from '@/components/BlankSlate.vue';
import markdown from '@/utils/markdown';
import CompanyInformationUpdateDialog from '@/components/dialogs/CompanyInformationUpdateDialog.vue';
import { useAuthStore } from '@/store/auth';

export default {
    name: 'CompanyDetail',
    data() {
        return {
            companyService: new CompanyService(),
            companyId: this.$route.params.companyId,
            breadcrumbs: [
                { label: 'Companies', to: this.$router.resolve({ name: 'CompanyList' }) },
                { label: 'Company Detail', disabled: true }
            ],
            company: { report_template: {} },
            authStore: useAuthStore(),
            companyInformation: []
        };
    },
    methods: {
        renderMarkdown(text) {
            return markdown.renderMarkdown(text);
        },
        getCompany() {
            this.companyService.getCompany(this.companyId).then((response) => {
                this.company = response.data;
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to delete this item?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.companyService.deleteCompanyInformation(this.$api, this.companyId, id).then(() => {
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
                    this.companyService.deleteCompany(this.$api, this.companyId).then(() => {
                        this.$router.push({ name: 'CompanyList' });
                    });
                }
            });
        },
        getCompanyInformation() {
            this.companyService.getCompanyInformation(this.companyId).then((response) => {
                this.companyInformation = response.data.results;
            });
        }
    },
    mounted() {
        this.getCompany();
        this.getCompanyInformation();
    },
    components: {
        CompanyInformationUpdateDialog,
        DetailCardWithIcon,
        CompanyInformationCreateDialog,
        CompanyUpdateDialog,
        CompanyTabMenu,
        BlankSlate
    }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start">
                <strong class="text-lg">{{ company.name }}</strong>
            </div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <CompanyUpdateDialog :company="company" @object-updated="getCompany"></CompanyUpdateDialog>
                <Button @click="confirmDialogDeleteCompany" outlined severity="danger" icon="fa fa-trash" label="Delete"></Button>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <CompanyTabMenu class="surface-card"></CompanyTabMenu>
            <div class="card border-noround-top">
                <div class="grid">
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Street" icon="fa-road" class="surface-ground" :text="company.street"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="City" icon="fa-city" class="surface-ground" :text="company.city"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Country" icon="fa-earth" class="surface-ground" :text="company.country"></DetailCardWithIcon>
                    </div>
                    <div class="col-12 md:col-3">
                        <DetailCardWithIcon title="Report Template" icon="fa-file" class="surface-ground" :text="company.report_template.name"></DetailCardWithIcon>
                    </div>
                </div>
                <div class="grid">
                    <div class="col-12">
                        <div class="grid">
                            <div class="col-6">
                                <p class="text-xl">Company Information</p>
                            </div>
                            <div class="col-6 flex justify-content-end">
                                <CompanyInformationCreateDialog @object-created="getCompanyInformation" :company-id="company.pk"></CompanyInformationCreateDialog>
                            </div>
                        </div>

                        <Card v-for="info in companyInformation" :key="info.pk" class="surface-ground mt-3">
                            <template #content>
                                <div v-html="renderMarkdown(info.text)"></div>
                            </template>
                            <template #footer>
                                <hr />
                                <div class="grid">
                                    <div class="col-12 md:col-6">
                                        {{ info.user.username }} on {{ info.date_created }}<span v-if="info.user_edit">; edited by {{ info.user_edit.username }} on {{ info.date_updated }}</span>
                                    </div>
                                    <div class="col-12 md:col-6">
                                        <div class="flex justify-content-end">
                                            <CompanyInformationUpdateDialog :information="info" @object-updated="getCompanyInformation"></CompanyInformationUpdateDialog>
                                            <Button size="small" icon="fa fa-trash" severity="danger" outlined @click="confirmDialogDelete(info.pk)"></Button>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </Card>
                        <BlankSlate v-if="companyInformation.length < 1" icon="fa fa-circle-info" text="No company information found!" title="No company information!"></BlankSlate>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
