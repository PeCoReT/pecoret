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
                name: 'AdvisoryDashboard',
                path: '/advisories/dashboard',
                component: () => import('@/views/pages/advisories/Dashboard.vue')
            },
            {
                name: 'AdvisoryLabelList',
                path: '/advisories/labels',
                component: () => import('@/views/pages/advisories/LabelList.vue')
            },
            {
                name: 'AdvisoryShareTokenList',
                path: '/advisories/:advisoryId/share-tokens',
                component: () => import('@/views/pages/advisories/ShareTokenList.vue')
            }
        ]
    }
];
export default advisoryRoutes;
