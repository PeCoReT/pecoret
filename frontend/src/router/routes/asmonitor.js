const asmonitorRoutes = [
    {
        path: '/attack-surface',
        children: [
            {
                path: '/attack-surface/programs',
                name: 'AttackSurfaceProgramList',
                component: () => import('@/views/pages/attack_surface/ProgramList.vue')
            },
            {
                path: '/attack-surface/programs/create',
                name: 'AttackSurfaceProgramCreate',
                component: () => import('@/views/pages/attack_surface/ProgramCreate.vue')
            },
            {
                path: '/attack-surface/programs/:programId/update',
                name: 'AttackSurfaceProgramUpdate',
                component: () => import('@/views/pages/attack_surface/ProgramUpdate.vue')
            },
            {
                path: '/attack-surface/tags',
                name: 'AttackSurfaceTagList',
                component: () => import('@/views/pages/attack_surface/TagList.vue')
            },
            {
                path: '/attack-surface/targets',
                name: 'AttackSurfaceTargetList',
                component: () => import('@/views/pages/attack_surface/TargetList.vue')
            },
            {
                path: '/attack-surface/scan-findings',
                name: 'AttackSurfaceScanFindingList',
                component: () => import('@/views/pages/attack_surface/ScanFindingList.vue')
            },
            {
                path: '/attack-surface/urls',
                name: 'AttackSurfaceURLList',
                component: () => import('@/views/pages/attack_surface/URLList.vue')
            },
            {
                path: '/attack-surface/urls/:urlId',
                name: 'AttackSurfaceURLDetail',
                component: () => import('@/views/pages/attack_surface/URLDetail.vue')
            },
            {
                path: '/attack-surface/scan-findings/:findingId',
                name: 'AttackSurfaceScanFindingDetail',
                component: () => import('@/views/pages/attack_surface/ScanFindingDetail.vue')
            },
            {
                path: '/attack-surface/targets/:targetId',
                name: 'AttackSurfaceTargetDetail',
                component: () => import('@/views/pages/attack_surface/TargetDetail.vue')
            },
            {
                path: '/attack-surface',
                name: 'AttackSurfaceSearch',
                component: () => import('@/views/pages/attack_surface/Search.vue')
            },
            {
                path: '/attack-surface/scanning/scan-tasks',
                name: 'AttackSurfaceScanTaskList',
                component: () => import('@/views/pages/attack_surface/ScanTaskList.vue')
            },
            {
                path: '/attack-surface/scanning/scan-tasks/:taskId',
                name: 'AttackSurfaceScanTaskDetail',
                component: () => import('@/views/pages/attack_surface/ScanTaskDetail.vue')
            },
            {
                path: '/attack-surface/findings',
                name: 'AttackSurfaceFindingList',
                component: () => import('@/views/pages/attack_surface/FindingList.vue')
            },
            {
                path: '/attack-surface/findings/create',
                name: 'AttackSurfaceFindingCreate',
                component: () => import('@/views/pages/attack_surface/FindingCreate.vue')
            },
            {
                path: '/attack-surface/findings/:findingId',
                name: 'AttackSurfaceFindingDetail',
                component: () => import('@/views/pages/attack_surface/FindingDetail.vue')
            },
            {
                path: '/attack-surface/findings/:findingId/update',
                name: 'AttackSurfaceFindingUpdate',
                component: () => import('@/views/pages/attack_surface/FindingUpdate.vue')
            },
            {
                path: '/attack-surface/scanning/scanners',
                name: 'AttackSurfaceScannerList',
                component: () => import('@/views/pages/attack_surface/ScannerList.vue')
            },
            {
                path: '/attack-surface/scoping',
                children: [
                    {
                        path: '/attack-surface/scoping',
                        name: 'AttackSurfaceScopeList',
                        component: () => import('@/views/pages/attack_surface/ScopeList.vue')
                    }
                ]
            }
        ]
    }
];

export default asmonitorRoutes;
