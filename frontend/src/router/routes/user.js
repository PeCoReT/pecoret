const userRoutes = [
    {
        path: '/user/settings',
        name: 'UserProfileSettings',
        component: () => import('@/views/pages/user/UserProfileSettings.vue')
    },
    {
        path: '/user/settings/notifications',
        name: 'UserNotificationSettings',
        component: () => import('@/views/pages/user/UserNotificationSettings.vue')
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
