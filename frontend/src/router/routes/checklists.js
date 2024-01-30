const checklistRoutes = [
    {
        path: '/checklists',
        children: [
            {
                path: '/checklists',
                name: 'ChecklistList',
                component: () => import('@/views/pages/checklists/ChecklistList.vue')
            },
            {
                path: '/checklists/create',
                name: 'ChecklistCreate',
                component: () => import('@/views/pages/checklists/ChecklistCreate.vue')
            },
            {
                path: '/checklists/categories',
                name: 'ChecklistCategoryList',
                component: () => import('@/views/pages/checklists/CategoryList.vue')
            },
            {
                path: '/checklists/categories/:categoryId',
                name: 'ChecklistCategoryDetail',
                component: () => import('@/views/pages/checklists/CategoryDetail.vue')
            },
            {
                path: '/checklists/:checklistId',
                name: 'ChecklistUpdate',
                component: () => import('@/views/pages/checklists/ChecklistUpdate.vue')
            }
        ]
    }
];

export default checklistRoutes;
