import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import adminRoutes from '@/router/routes/admin';
import projectRoutes from '@/router/routes/projects';
import baseRoutes from '@/router/routes/base';
import checklistRoutes from '@/router/routes/checklists';
import companyRoutes from '@/router/routes/companies';
import vulnerabilityTemplateRoutes from '@/router/routes/vulnerabilityTemplates';
import advisoryRoutes from '@/router/routes/advisories';
import userRoutes from '@/router/routes/user';
import asmonitorRoutes from '@/router/routes/asmonitor';
import technologyRoutes from "@/router/routes/technologies";

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
                ...advisoryRoutes,
                ...vulnerabilityTemplateRoutes,
                ...checklistRoutes,
                ...companyRoutes,
                ...userRoutes,
                ...asmonitorRoutes,
                ...technologyRoutes
            ]
        },
        ...baseRoutes
    ]
});

export default router;
