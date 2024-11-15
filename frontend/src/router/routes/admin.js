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
                path: '/admins/project-types',
                name: 'ProjectTypeList',
                component: () => import('@/views/pages/admin/ProjectTypeList.vue')
            },
            {
                path: '/admin/attack-surface/scanners',
                name: 'AdminAttackSurfaceScannerList',
                component: () => import('@/views/pages/admin/ASScannerList.vue')
            },
            {
                path: '/admin/attack-surface/scan-types',
                name: 'AdminAttackSurfaceScanTypeList',
                component: () => import('@/views/pages/admin/ASScanTypeList.vue')
            }
        ]
    }
];

export default adminRoutes;
