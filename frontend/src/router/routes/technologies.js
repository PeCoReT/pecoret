const technologyRoutes = [
    {
        path: '/technologies',
        name: 'TechnologyList',
        component: () => import('@/views/pages/technologies/TechnologyList.vue')
    }
];

export default technologyRoutes;
