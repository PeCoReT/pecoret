const technologyRoutes = [
    {
        path: '/knowledge-base/technologies',
        name: 'TechnologyList',
        component: () => import('@/views/pages/knowledgebase/TechnologyList.vue')
    },
    {
        path: '/knowledge-base/technologies/create',
        name: 'TechnologyCreate',
        component: () => import('@/views/pages/knowledgebase/TechnologyCreate.vue')
    },
    {
        path: '/knowledge-base/technologies/:techId',
        name: 'TechnologyUpdate',
        component: () => import('@/views/pages/knowledgebase/TechnologyUpdate.vue')
    }
];

export default technologyRoutes;
