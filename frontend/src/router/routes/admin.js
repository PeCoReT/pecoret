const adminRoutes = [
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
            },
            {
                path: '/admins/settings',
                name: 'AdminSettings',
                component: () => import('@/views/pages/admin/Settings.vue')
            }
        ]
    }
];

export default adminRoutes;
