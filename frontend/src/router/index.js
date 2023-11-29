import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'Home',
                    component: () => import('@/views/Home.vue')
                },

                {
                    path: '/admin',
                    children: [
                        {
                            path: '/admin/users',
                            name: 'UserList',
                            component: () => import('@/views/pages/admin/UserList.vue')
                        },
                        {
                            path: '/admin/report-templates',
                            name: 'ReportTemplateList',
                            component: () => import('@/views/pages/admin/ReportTemplateList.vue')
                        },
                        {
                            path: '/admins/project-types',
                            name: 'ProjectTypeList',
                            component: () => import('@/views/pages/admin/ProjectTypeList.vue')
                        }
                    ]
                },
                {
                    path: '/projects',
                    children: [
                        {
                            path: '/projects',
                            name: 'ProjectList',
                            component: () => import('@/views/pages/projects/ProjectList.vue')
                        },
                        {
                            path: '/projects/:projectId',
                            children: [
                                {
                                    path: '/projects/:projectId',
                                    name: 'ProjectDetail',
                                    component: () => import('@/views/pages/projects/ProjectDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings',
                                    name: 'FindingList',
                                    component: () => import('@/views/pages/projects/findings/FindingList.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/create',
                                    name: 'FindingCreate',
                                    component: () => import('@/views/pages/projects/findings/FindingCreate.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId',
                                    name: 'FindingDetail',
                                    component: () => import('@/views/pages/projects/findings/FindingDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/comments',
                                    name: 'FindingCommentList',
                                    component: () => import('@/views/pages/projects/findings/CommentList.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/scores',
                                    name: 'FindingScoreList',
                                    component: () => import('@/views/pages/projects/findings/ScoreList.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/timelines',
                                    name: 'FindingTimelineList',
                                    component: () => import('@/views/pages/projects/findings/TimelineList.vue')
                                },
                                {
                                    path: '/projects/:projectId/web-applications',
                                    name: 'WebApplicationList',
                                    component: () => import('@/views/pages/projects/assets/WebApplicationList.vue')
                                },
                                {
                                    path: '/projects/:projectId/web-applications/:assetId',
                                    name: 'WebApplicationDetail',
                                    component: () => import('@/views/pages/projects/assets/WebApplicationDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/hosts',
                                    name: 'HostList',
                                    component: () => import('@/views/pages/projects/assets/HostList.vue')
                                },
                                {
                                    path: '/projects/:projectId/hosts/:assetId',
                                    name: 'HostDetail',
                                    component: () => import('@/views/pages/projects/assets/HostDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/mobile-applications',
                                    name: 'MobileApplicationList',
                                    component: () => import('@/views/pages/projects/assets/MobileApplicationList.vue')
                                },
                                {
                                    path: '/projects/:projectId/mobile-applications/:assetId',
                                    name: 'MobileApplicationDetail',
                                    component: () => import('@/views/pages/projects/assets/MobileApplicationDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/thick-clients',
                                    name: 'ThickClientList',
                                    component: () => import('@/views/pages/projects/assets/ThickClientList.vue')
                                },
                                {
                                    path: '/projects/:projectId/thick-clients/:assetId',
                                    name: 'ThickClientDetail',
                                    component: () => import('@/views/pages/projects/assets/ThickClientDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/team',
                                    name: 'ContributorList',
                                    component: () => import('@/views/pages/projects/management/ContributorList.vue')
                                },
                                {
                                    path: '/projects/:projectId/contacts',
                                    name: 'ContactList',
                                    component: () => import('@/views/pages/projects/management/ContactList.vue')
                                },
                                {
                                    path: '/projects/:projectId/user-accounts',
                                    name: 'UserAccountList',
                                    component: () => import('@/views/pages/projects/management/UserAccountList.vue')
                                },
                                {
                                    path: '/projects/:projectId/vulnerabilities',
                                    name: 'VulnerabilityList',
                                    component: () => import('@/views/pages/projects/vulnerabilities/VulnerabilityList.vue')
                                },
                                {
                                    path: '/projects/:projectId/vulnerabilities/create',
                                    name: 'VulnerabilityCreate',
                                    component: () => import('@/views/pages/projects/vulnerabilities/VulnerabilityCreate.vue')
                                },
                                {
                                    path: '/projects/:projectId/vulnerabilities/:vulnerabilityId/update',
                                    name: 'VulnerabilityUpdate',
                                    component: () => import('@/views/pages/projects/vulnerabilities/VulnerabilityUpdate.vue')
                                },
                                {
                                    path: '/projects/:projectId/reports',
                                    name: 'ReportList',
                                    component: () => import('@/views/pages/projects/reports/ReportList.vue')
                                },
                                {
                                    path: '/projects/:projectId/reports/:reportId',
                                    name: 'ReportDetail',
                                    component: () => import('@/views/pages/projects/reports/ReportDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/reports/:reportId/version-history',
                                    name: 'ReportVersionHistoryList',
                                    component: () => import('@/views/pages/projects/reports/VersionHistoryList.vue')
                                },
                                {
                                    path: '/projects/:projectId/reports/:reportId/documents',
                                    name: 'ReportDocumentList',
                                    component: () => import('@/views/pages/projects/reports/ReportDocumentList.vue')
                                },
                                {
                                    path: '/projects/:projectId/services',
                                    name: 'ServiceList',
                                    component: () => import('@/views/pages/projects/assets/ServiceList.vue')
                                },
                                {
                                    path: '/projects/:projectId/services/:assetId',
                                    name: 'ServiceDetail',
                                    component: () => import('@/views/pages/projects/assets/ServiceDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/update',
                                    name: 'FindingUpdate',
                                    component: () => import('@/views/pages/projects/findings/FindingUpdate.vue')
                                },
                                {
                                    path: '/projects/:projectId/checklists',
                                    name: 'ProjectChecklistList',
                                    component: () => import('@/views/pages/projects/checklists/ChecklistList.vue')
                                },
                                {
                                    path: '/projects/:projectId/files',
                                    name: 'ProjectFileList',
                                    component: () => import('@/views/pages/projects/management/ProjectFileList.vue')
                                },
                                {
                                    path: '/projects/:projectId/commands',
                                    name: 'ProjectCommandList',
                                    component: () => import('@/views/pages/projects/commands/CommandList.vue')
                                },
                                {
                                    path: '/projects/:projectId/scopes',
                                    name: 'ProjectScopeList',
                                    component: () => import('@/views/pages/projects/scope/ScopeList.vue')
                                },
                                {
                                    path: '/projects/:projectId/notes',
                                    name: 'ProjectNoteList',
                                    component: () => import('@/views/pages/projects/notes/NoteList.vue')
                                }
                            ]
                        }
                    ]
                },
                {
                    path: '/advisory-management',
                    children: [
                        {
                            name: 'AdvisoryManagementLabelList',
                            path: '/advisory-management/labels',
                            component: () => import('@/views/pages/advisories/LabelList.vue')
                        },
                        {
                            name: 'AdvisoryManagementDashboard',
                            path: '/advisory-management',
                            component: () => import('@/views/pages/advisories/management/Dashboard.vue')
                        }
                    ]
                },
                {
                    path: '/advisories',
                    children: [
                        {
                            name: 'AdvisoryList',
                            path: '/advisories',
                            component: () => import('@/views/pages/advisories/AdvisoryList.vue')
                        },
                        {
                            name: 'AdvisoryInbox',
                            path: '/advisories/inbox',
                            component: () => import('@/views/pages/advisories/AdvisoryInbox.vue')
                        },
                        {
                            name: 'AdvisoryCreate',
                            path: '/advisories/create',
                            component: () => import('@/views/pages/advisories/AdvisoryCreate.vue')
                        },
                        {
                            name: 'AdvisoryDetail',
                            path: '/advisories/:advisoryId',
                            component: () => import('@/views/pages/advisories/AdvisoryDetail.vue')
                        },
                        {
                            name: 'AdvisoryUpdate',
                            path: '/advisories/:advisoryId/update',
                            component: () => import('@/views/pages/advisories/AdvisoryUpdate.vue')
                        },
                        {
                            name: 'AdvisoryTimelineList',
                            path: '/advisories/:advisoryId/timeline',
                            component: () => import('@/views/pages/advisories/TimelineList.vue')
                        },
                        {
                            name: 'AdvisoryCommentList',
                            path: '/advisories/:advisoryId/comments',
                            component: () => import('@/views/pages/advisories/CommentList.vue')
                        },
                        {
                            name: 'AdvisoryMembershipList',
                            path: '/advisories/:advisoryId/memberships',
                            component: () => import('@/views/pages/advisories/MembershipList.vue')
                        },
                        {
                            name: 'AdvisoryProofList',
                            path: '/advisories/:advisoryId/proofs',
                            component: () => import('@/views/pages/advisories/ProofList.vue')
                        }
                    ]
                },

                {
                    path: '/vulnerability-templates',
                    name: 'VulnerabilityTemplateList',
                    component: () => import('@/views/pages/vulnerability_templates/VulnerabilityTemplateList.vue')
                },
                {
                    path: '/vulnerability-templates/create',
                    name: 'VulnerabilityTemplateCreate',
                    component: () => import('@/views/pages/vulnerability_templates/VulnerabilityTemplateCreate.vue')
                },
                {
                    path: '/vulnerability-templates/:templateId',
                    name: 'VulnerabilityTemplateUpdate',
                    component: () => import('@/views/pages/vulnerability_templates/VulnerabilityTemplateUpdate.vue')
                },
                {
                    path: '/vulnerability-templates/:templateId/:language',
                    name: 'VulnerabilityTemplateTranslationUpdate',
                    component: () => import('@/views/pages/vulnerability_templates/TranslationUpdate.vue')
                },
                {
                    path: '/companies',
                    children: [
                        {
                            path: '/companies',
                            name: 'CompanyList',
                            component: () => import('@/views/pages/companies/CompanyList.vue')
                        },
                        {
                            path: '/companies/:companyId',
                            name: 'CompanyDetail',
                            component: () => import('@/views/pages/companies/CompanyDetail.vue')
                        },
                        {
                            path: '/companies/:companyId/contacts',
                            name: 'CompanyContactList',
                            component: () => import('@/views/pages/companies/CompanyContactList.vue')
                        }
                    ]
                },
                {
                    path: '/user/settings',
                    name: 'UserSettingsDetail',
                    component: () => import('@/views/pages/settings/UserSettingsDetail.vue')
                },
                {
                    path: '/user/settings/profile',
                    name: 'UserProfileSettings',
                    component: () => import('@/views/pages/settings/UserProfileSettings.vue')
                },
                {
                    path: '/user/api-tokens',
                    name: 'APITokenList',
                    component: () => import('@/views/pages/APITokenList.vue')
                },
                {
                    path: '/user/change-email/:uid/:token',
                    name: 'UserChangeEmailConfirm',
                    component: () => import('@/views/pages/UserChangeEmailConfirm.vue')
                }
            ]
        },

        {
            path: '/login',
            name: 'Login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/reset_password',
            name: 'ResetPassword',
            component: () => import('@/views/pages/auth/ResetPassword.vue')
        },
        {
            path: '/account-activation/:uid/:token',
            name: 'AccountActivation',
            component: () => import('@/views/pages/auth/AccountActivation.vue')
        }
    ]
});

export default router;
