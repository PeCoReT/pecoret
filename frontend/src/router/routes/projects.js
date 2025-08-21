const projectRoutes = [
    {
        path: '/projects',
        children: [
            {
                path: '/projects',
                children: [
                    {
                        name: 'ProjectList',
                        path: '/projects',
                        component: () => import('@/views/pages/projects/ProjectList.vue')
                    },
                    {
                        path: '/projects/create',
                        name: 'ProjectCreate',
                        component: () => import('@/views/pages/projects/ProjectCreate.vue')
                    }
                ]
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
                        path: '/projects/:projectId/update',
                        name: 'ProjectUpdate',
                        component: () => import('@/views/pages/projects/ProjectUpdate.vue')
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
                        path: '/projects/:projectId/findings/create',
                        name: 'FindingCreate',
                        component: () => import('@/views/pages/projects/findings/FindingCreate.vue')
                    },
                    {
                        path: '/projects/:projectId/findings/:findingId/comments',
                        name: 'FindingCommentList',
                        component: () => import('@/views/pages/projects/findings/CommentList.vue')
                    },
                    {
                        path: '/projects/:projectId/findings/:findingId/retest',
                        name: 'FindingRetest',
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
                        path: '/projects/:projectId/assets',
                        name: 'AssetList',
                        component: () => import('@/views/pages/projects/assets/AssetList.vue')
                    },
                    {
                        path: '/projects/:projectId/assets/:assetId',
                        name: 'AssetDetail',
                        component: () => import('@/views/pages/projects/assets/AssetDetail.vue')
                    },
                    {
                        path: '/projects/:projectId/assets/:assetId/update',
                        name: 'AssetUpdate',
                        component: () => import('@/views/pages/projects/assets/AssetUpdate.vue')
                    },
                    {
                        path: '/projects/:projectId/assets/create',
                        name: 'AssetCreate',
                        component: () => import('@/views/pages/projects/assets/AssetCreate.vue')
                    },
                    {
                        path: '/projects/:projectId/team',
                        name: 'ContributorList',
                        component: () => import('@/views/pages/projects/management/ContributorList.vue')
                    },
                    {
                        path: '/projects/:projectId/team/create',
                        name: 'ContributorCreate',
                        component: () => import('@/views/pages/projects/management/ContributorCreate.vue')
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
                        path: '/projects/:projectId/user-accounts/create',
                        name: 'UserAccountCreate',
                        component: () => import('@/views/pages/projects/management/UserAccountCreate.vue')
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
    }
];

export default projectRoutes;
