import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import adminRoutes from '@/router/routes/admin';
import projectRoutes from '@/router/routes/projects';
import advisoryManagementRoutes from '@/router/routes/advisoryManagement';
import baseRoutes from '@/router/routes/base';
import checklistRoutes from '@/router/routes/checklists';
import companyRoutes from '@/router/routes/companies';
import vulnerabilityTemplateRoutes from '@/router/routes/vulnerabilityTemplates';
import advisoryRoutes from '@/router/routes/advisories';
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

                ...adminRoutes,
                ...projectRoutes,
                ...advisoryManagementRoutes,
                ...advisoryRoutes,
                ...vulnerabilityTemplateRoutes,
                ...checklistRoutes,
                ...companyRoutes,
                ...userRoutes
            ]
        },
        ...baseRoutes
    ]
});

export default router;
