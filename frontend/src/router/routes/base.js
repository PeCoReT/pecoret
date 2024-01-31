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
        path: '/account-activation/:uid/:token',
        name: 'AccountActivation',
        component: () => import('@/views/pages/auth/AccountActivation.vue')
    }
]

export default baseRoutes;
