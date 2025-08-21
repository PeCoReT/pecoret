import { createRouter, createWebHashHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import baseRoutes from '@/router/routes/base';
import projectRoutes from '@/router/routes/projects';
import advisoryRoutes from '@/router/routes/advisories';
import checklistRoutes from '@/router/routes/checklists';
import vulnerabilityTemplateRoutes from '@/router/routes/vulnerabilityTemplates';
import technologyRoutes from '@/router/routes/technologies';
import asmonitorRoutes from '@/router/routes/asmonitor';
import companyRoutes from '@/router/routes/companies';
import userRoutes from '@/router/routes/user';

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'Home',
                    component: () => import('@/views/Home.vue')
                },
                ...projectRoutes,
                ...advisoryRoutes,
                ...vulnerabilityTemplateRoutes,
                ...checklistRoutes,
                ...companyRoutes,
                ...userRoutes,
                ...asmonitorRoutes,
                ...technologyRoutes
            ]
        },
        ...baseRoutes,
        {
            name: 'AdvisoryShareTokenDownload',
            path: '/advisories/:advisoryId/download/:token',
            meta: {
                auth: true
            },
            component: () => import('@/views/pages/advisories/ShareTokenAdvisoryDownload.vue')
        },
        {
            path: '/:catchAll(.*)',
            meta: {
                auth: false
            },
            component: () => import('@/views/pages/404.vue')
        }
    ]
});

export default router;
