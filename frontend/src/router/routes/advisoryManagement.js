const advisoryManagementRoutes = [
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
    }
];

export default advisoryManagementRoutes;
