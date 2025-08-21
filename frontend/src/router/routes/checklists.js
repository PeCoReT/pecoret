const checklistRoutes = [
    {
        path: '/knowledge-base/checklists',
        children: [
            {
                path: '/knowledge-base/checklists',
                name: 'ChecklistList',
                component: () => import('@/views/pages/knowledgebase/checklists/ChecklistList.vue')
            },
            {
                path: '/knowledge-base/checklists/create',
                name: 'ChecklistCreate',
                component: () => import('@/views/pages/knowledgebase/checklists/ChecklistCreate.vue')
            },
            {
                path: '/knowledge-base/checklists/categories',
                name: 'ChecklistCategoryList',
                component: () => import('@/views/pages/knowledgebase/checklists/CategoryList.vue')
            },
            {
                path: '/knowledge-base/checklists/categories/create',
                name: 'ChecklistCategoryCreate',
                component: () => import('@/views/pages/knowledgebase/checklists/CategoryCreate.vue')
            },
            {
                path: '/knowledge-base/checklists/categories/:categoryId/update',
                name: 'ChecklistCategoryUpdate',
                component: () => import('@/views/pages/knowledgebase/checklists/CategoryUpdate.vue')
            },
            {
                path: '/knowledge-base/checklists/:checklistId',
                name: 'ChecklistUpdate',
                component: () => import('@/views/pages/knowledgebase/checklists/ChecklistUpdate.vue')
            },
            {
                path: '/knowledge-base/checklists/items',
                children: [
                    {
                        path: '/knowledge-base/checklists/items',
                        name: 'ChecklistItemList',
                        component: () => import('@/views/pages/knowledgebase/checklists/ItemList.vue')
                    },
                    {
                        path: '/knowledge-base/checklists/items/:itemId',
                        name: 'ChecklistItemUpdate',
                        component: () => import('@/views/pages/knowledgebase/checklists/ItemUpdate.vue')
                    },
                    {
                        path: '/knowledge-base/checklists/items/create',
                        name: 'ChecklistItemCreate',
                        component: () => import('@/views/pages/knowledgebase/checklists/ItemCreate.vue')
                    }
                ]
            }
        ]
    }
];

export default checklistRoutes;
