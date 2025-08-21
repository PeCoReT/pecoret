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
                path: '/companies/create',
                name: 'CompanyCreate',
                component: () => import('@/views/pages/companies/CompanyCreate.vue')
            },
            {
                path: '/companies/:companyId',
                name: 'CompanyDetail',
                component: () => import('@/views/pages/companies/CompanyDetail.vue')
            },
            {
                path: '/companies/:companyId/update',
                name: 'CompanyUpdate',
                component: () => import('@/views/pages/companies/CompanyUpdate.vue')
            },
            {
                path: '/companies/:companyId/contacts',
                name: 'CompanyContactList',
                component: () => import('@/views/pages/companies/CompanyContactList.vue')
            },
            {
                path: '/companies/:companyId/contacts/create',
                name: 'CompanyContactCreate',
                component: () => import('@/views/pages/companies/CompanyContactCreate.vue')
            },
            {
                path: '/companies/:companyId/contacts/:contactId/update',
                name: 'CompanyContactUpdate',
                component: () => import('@/views/pages/companies/CompanyContactUpdate.vue')
            }
        ]
    }
];

export default companyRoutes;
