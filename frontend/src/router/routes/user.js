const userRoutes = [
    {
        path: '/user/settings',
        name: 'UserSettingsDetail',
        component: () => import('@/views/pages/settings/UserSettingsDetail.vue')
    },
    {
        path: '/user/settings/profile',
        name: 'UserProfileSettings',
        component: () => import('@/views/pages/settings/UserProfileSettings.vue')
    },
    {
        path: '/user/api-tokens',
        name: 'APITokenList',
        component: () => import('@/views/pages/user/APITokenList.vue')
    },
    {
        path: '/user/change-email/:uid/:token',
        name: 'UserChangeEmailConfirm',
        component: () => import('@/views/pages/user/UserChangeEmailConfirm.vue')
    }
];

export default userRoutes;
