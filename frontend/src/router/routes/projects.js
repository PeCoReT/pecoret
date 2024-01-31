const projectRoutes = [
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
                        path: '/projects/:projectId/findings/:findingId',
                        name: 'FindingDetail',
                        component: () => import('@/views/pages/projects/findings/FindingDetail.vue')
                    },
                    {
                        path: '/projects/:projectId/findings/:findingId/comments',
                        name: 'FindingCommentList',
                        props: true,
                        component: () => import('@/views/pages/projects/findings/CommentList.vue')
                    },
                    {
                        path: '/projects/:projectId/findings/:findingId/retest',
                        name: 'FindingRetest',
                        props: true,
                        component: () => import('@/views/pages/projects/findings/FindingRetest.vue')
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
                    },
                    {
                        path: '/projects/:projectId/generic-assets',
                        name: 'GenericAssetList',
                        component: () => import('@/views/pages/projects/assets/GenericAssetList.vue')
                    },
                    {
                        path: '/projects/:projectId/generic-assets/:assetId',
                        name: 'GenericAssetDetail',
                        component: () => import('@/views/pages/projects/assets/GenericAssetDetail.vue')
                    }
                ]
            }
        ]
    }
];

export default projectRoutes;
