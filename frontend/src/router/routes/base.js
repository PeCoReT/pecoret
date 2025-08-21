const baseRoutes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/pages/auth/Login.vue')
    },
    {
        path: '/reset_password',
        name: 'ResetPassword',
        component: () => import('@/views/pages/auth/ResetPassword.vue')
    },
    {
        path: '/reset-password/:token',
        name: 'ResetPasswordConfirm',
        component: () => import('@/views/pages/auth/ResetPasswordConfirm.vue')
    }
];

export default baseRoutes;
