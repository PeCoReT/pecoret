const technologyRoutes = [
    {
        path: '/technologies',
        name: 'TechnologyList',
        component: () => import('@/views/pages/knowledgebase/TechnologyList.vue')
    }
];

export default technologyRoutes;
