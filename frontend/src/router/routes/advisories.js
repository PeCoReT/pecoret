const advisoryRoutes = [
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
    }
];
export default advisoryRoutes;
