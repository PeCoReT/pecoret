<script>
import { BlankSlate } from '@/components/blankslate';
import { CommentCard } from '@/partials/common';
import { useAuthStore } from '@/store/auth';
import { MarkdownEditor } from '@/components/editor';
import { DetailCardWithIcon } from '@/components/card';
import { CompanyTabMenu } from '@/partials/companies';
import { Paginator } from '@/components/paginator';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import PageHeader from '@/components/typography/PageHeader.vue';

export default {
    name: 'CompanyDetail',
    data() {
        return {
            companyId: this.$route.params.companyId,
            company: { report_template: {} },
            authStore: useAuthStore(),
            companyInformation: [],
            pagination: { limit: 25, page: 1 },
            totalRecords: 0,
            logoUrl: null,
            newInformationText: null,
            showNewInfo: false
        };
    },
    methods: {
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
                this.showNewInfo = false;
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
        PageHeader,
        ContainerLayout,
        MarkdownEditor,
        DetailCardWithIcon,
        CompanyTabMenu,
        BlankSlate,
        CommentCard,
        Paginator,
        Button
    }
};
</script>
<template>
    <ContainerLayout>
        <!-- Company Tabs -->
        <template #pre-content>
            <CompanyTabMenu class="mb-6" />
        </template>

        <!-- Company Header Card -->
        <Card class="col-span-12 p-6 shadow-sm rounded-2xl">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
                <!-- Logo & Company Info -->
                <div class="flex items-center gap-6">
                    <div v-if="!company.has_logo" class="w-24 h-24 rounded-full bg-muted flex items-center justify-center">
                        <span class="text-sm text-muted-foreground">No Logo</span>
                    </div>
                    <div v-else class="w-24 h-24 rounded-full overflow-hidden border">
                        <img :src="logoUrl" alt="company logo" class="object-cover w-full h-full" />
                    </div>

                    <div>
                        <h1 class="text-2xl font-bold tracking-tight">{{ company.name }}</h1>
                        <p class="text-muted-foreground text-sm">{{ company.street }}, {{ company.city }}, {{ company.country }}</p>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex gap-3">
                    <Button :href="$router.resolve({ name: 'CompanyUpdate', params: { companyId } }).href" as="a" variant="outline"> <i class="fa fa-edit mr-2"></i> Edit </Button>
                    <Button variant="destructive" @click="confirmDialogDeleteCompany"> <i class="fa fa-trash mr-2"></i> Delete </Button>
                </div>
            </div>

            <!-- Report Template -->
            <div class="mt-6">
                <h2 class="text-lg font-semibold mb-1">Report Template</h2>
                <p class="text-muted-foreground text-sm">
                    {{ company.report_template || 'No template set' }}
                </p>
            </div>
        </Card>

        <!-- Company Information Section -->
        <div class="col-span-12 mt-10 space-y-6">
            <div class="flex items-center justify-between">
                <PageHeader>Company Information</PageHeader>

                <!-- Toggle New Information form -->
                <Button variant="outline" @click="showNewInfo = !showNewInfo">
                    <i :class="showNewInfo ? 'fa fa-times mr-2' : 'fa fa-plus mr-2'"></i>
                    {{ showNewInfo ? 'Cancel' : 'Add New Information' }}
                </Button>
            </div>

            <!-- New Information Form (hidden until toggled) -->
            <Card v-if="showNewInfo" class="p-6 rounded-xl shadow-sm">
                <Form>
                    <Field label="New Information">
                        <MarkdownEditor v-model="newInformationText" max-height="200px" />
                    </Field>
                    <div class="mt-4 flex gap-2">
                        <Button class="flex-1" variant="outline" type="button" @click="showNewInfo = false"> Cancel </Button>
                        <Button class="flex-1" @click="createCompanyInformation"> <i class="fa fa-paper-plane mr-2"></i> Save </Button>
                    </div>
                </Form>
            </Card>

            <!-- Existing Information -->
            <div v-if="companyInformation.length > 0" class="space-y-3">
                <CommentCard v-for="info in companyInformation" :key="info.pk" :comment="info" @onDelete="confirmDialogDelete" @comment-edited="companyInformationUpdated" />
            </div>

            <!-- Pagination -->
            <Paginator v-if="companyInformation.length > 0" :rows="pagination.limit" :totalRecords="totalRecords" class="justify-center flex mt-6" @page="onPage" />

            <!-- Blank State -->
            <Card v-else class="p-6 rounded-xl shadow-sm">
                <BlankSlate icon="fa fa-circle-info" title="No company information" text="This company does not yet have any information." />
                <div class="flex justify-center">
                    <Button @click="showNewInfo = true"> <i class="fa fa-plus mr-2"></i> Add First Information </Button>
                </div>
            </Card>
        </div>
    </ContainerLayout>
</template>
