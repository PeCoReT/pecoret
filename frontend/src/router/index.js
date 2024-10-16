import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import baseRoutes from '@/router/routes/base';
import projectRoutes from '@/router/routes/projects';
import advisoryRoutes from '@/router/routes/advisories';
import adminRoutes from '@/router/routes/admin';
import checklistRoutes from '@/router/routes/checklists';
import vulnerabilityTemplateRoutes from '@/router/routes/vulnerabilityTemplates';
import technologyRoutes from '@/router/routes/technologies';
import asmonitorRoutes from '@/router/routes/asmonitor';
import companyRoutes from '@/router/routes/companies';
import userRoutes from '@/router/routes/user';

const router = createRouter({
    history: createWebHistory(),
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
                ...adminRoutes,
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
            component: () => import('@/views/pages/advisories/ShareTokenAdvisoryDownload.vue')
        },
        {
            path: '/:catchAll(.*)',
            component: () => import('@/views/pages/404.vue')
        }
    ]
});

export default router;
