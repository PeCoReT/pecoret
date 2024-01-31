const companyRoutes = [
    {
        path: '/companies',
        children: [
            {
                path: '/companies',
                name: 'CompanyList',
                component: () => import('@/views/pages/companies/CompanyList.vue')
            },
            {
                path: '/companies/:companyId',
                name: 'CompanyDetail',
                component: () => import('@/views/pages/companies/CompanyDetail.vue')
            },
            {
                path: '/companies/:companyId/contacts',
                name: 'CompanyContactList',
                component: () => import('@/views/pages/companies/CompanyContactList.vue')
            }
        ]
    }
];

export default companyRoutes;
