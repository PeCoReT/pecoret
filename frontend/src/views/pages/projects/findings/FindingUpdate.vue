<script>
import FindingService from '@/service/FindingService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import UserAccountService from '@/service/UserAccountService';

export default {
    name: 'FindingUpdate',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({
                        name: 'FindingList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Finding Detail',
                    to: this.$router.resolve({
                        name: 'FindingDetail',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Update',
                    disabled: true
                }
            ],
            loading: false,
            service: new FindingService(),
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            model: {},
            dataLoaded: false,
            userAccountChoices: [],
            accountService: new UserAccountService()
        };
    },
    mounted() {
        this.onUserAccountFocus();
        this.getItem();
    },
    methods: {
        getItem() {
            this.service.getFinding(this.projectId, this.findingId).then((response) => {
                this.model = response.data;
                this.dataLoaded = true;
            });
        },
        onUserAccountFocus() {
            if (this.userAccountChoices.length) {
                return;
            }
            this.accountService.getAccounts(this.$api, this.projectId).then((response) => {
                this.userAccountChoices = response.data.results;
            });
        },
        patchFinding() {
            this.loading = true;
            let data = {
                name: this.model.name,
                exclude_from_report: this.model.exclude_from_report,
                recommendation: this.model.recommendation,
                date_retest: this.model.date_retest,
                retest_results: this.model.retest_results
            };
            if (this.model.user_account) {
                data['user_account'] = this.model.user_account.pk;
            }
            this.service
                .patchFinding(this.$api, this.projectId, this.findingId, data)
                .then(() => {
                    this.$router.push({
                        name: 'FindingDetail',
                        params: {
                            projectId: this.projectId,
                            findingId: this.findingId
                        }
                    });
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: { MarkdownEditor }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <Breadcrumb :model="breadcrumbs"></Breadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card" v-if="dataLoaded">
                <div class="flex flex-column gap-2 mt-3">
                    <label for="name">Name</label>
                    <InputText id="name" type="text" v-model="model.name" label="Name"></InputText>
                </div>
                <div class="flex flex-column gap-2 mt-3">
                    <div class="flex align-items-center">
                        <Checkbox v-model="model.exclude_from_report" binary id="exclude_from_report"></Checkbox>
                        <label for="exclude_from_report" class="ml-2"> Exclude From Report?</label>
                    </div>
                </div>
                <div class="flex flex-column gap-2 mt-3">
                    <label for="account">Account</label>
                    <Dropdown :options="userAccountChoices" optionLabel="username" v-model="model.user_account"></Dropdown>
                </div>

                <div class="flex flex-column gap-2 mt-3">
                    <label for="recommendation">Recommendation</label>
                    <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
                </div>
                <div class="flex flex-column gap-2 mt-3">
                    <label for="date_retested">Date Retested</label>
                    <Calendar v-model="model.date_retested" id="date_retested"></Calendar>
                </div>

                <div class="flex flex-column gap-2 mt-3">
                    <label for="retest">Retest Summary</label>
                    <MarkdownEditor v-model="model.retest_results"></MarkdownEditor>
                </div>
                <div class="flex flex-column gap-2 mt-3">
                    <div class="flex justify-content-end">
                        <Button label="Save" :loading="loading" @click="patchFinding"></Button>
                    </div>
                </div>
            </div>
            <div class="card" v-else>
                <Skeleton class="mb-2"></Skeleton>
                <Skeleton width="10rem" class="mb-2"></Skeleton>
                <Skeleton height="2rem" class="mb-2"></Skeleton>
                <Skeleton width="8rem" height="4rem"></Skeleton>
            </div>
        </div>
    </div>
</template>