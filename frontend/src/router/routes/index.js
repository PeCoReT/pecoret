import projectRoutes from '@/router/routes/projects';
import adminRoutes from '@/router/routes/admin';
import advisoryRoutes from '@/router/routes/advisories';
import baseRoutes from '@/router/routes/base';
import checklistRoutes from '@/router/routes/checklists';
import companyRoutes from '@/router/routes/companies';
import vulnerabilityTemplateRoutes from '@/router/routes/vulnerabilityTemplates';
import userRoutes from '@/router/routes/user';

const bundledRoutes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/Home.vue')
    },
    ...projectRoutes,
    ...adminRoutes,
    ...advisoryRoutes,
    ...baseRoutes,
    ...checklistRoutes,
    ...companyRoutes,
    ...vulnerabilityTemplateRoutes,
    ...userRoutes
];

export default bundledRoutes;
