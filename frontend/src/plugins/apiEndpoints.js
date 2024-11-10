const endpoints = {
    attackSurfaceUrls: '/attack-surface/urls/',
    authCheck: '/auth/check/',
    authLogin: '/auth/login/',
    authLogout: '/auth/logout/',
    authResetPassword: '/users/reset_password/',
    authActivation: '/users/activation',

    projectList: '/projects/',
    projectDetail: '/projects/{pk}/',
    projectsAvailableLanguages: '/projects/available-languages/',
    projectMembershipsMe: '/projects/{pk}/memberships/me/',
    projectsUnpinProject: '/projects/{pk}/unpin_project/',
    projectsPinProject: '/projects/{pk}/pin_project/',
    projectsStatusFindingDashboard: '/projects/{pk}/stats_finding_dashboard/',
    projectsContactList: '/projects/{projectPk}/contacts/',
    projectsContactDetail: '/projects/{projectPk}/contacts/{pk}/',

    pMembershipList: '/projects/{projectPk}/memberships/',
    pMembershipDetail: '/projects/{projectPk}/memberships/{pk}/',

    pCommandList: '/projects/{projectPk}/commands/',
    pCommandDetail: '/projects/{projectPk}/commands/{pk}/',

    pNoteList: '/projects/{projectPk}/notes/',
    pNoteDetail: '/projects/{projectPk}/notes/{pk}/',
    pNoteLock: '/projects/{projectPk}/notes/{pk}/lock/',
    pNoteUnlock: '/projects/{projectPk}/notes/{pk}/unlock/',

    pScopeList: '/projects/{projectPk}/scopes/',
    pScopeDetail: '/projects/{projectPk}/scopes/{pk}/',

    // assets
    pGenericAssetList: '/projects/{projectPk}/generic-assets/',
    pGenericAssetDetail: '/projects/{projectPk}/generic-assets/{pk}/',
    pThickClientList: '/projects/{projectPk}/thick-clients/',
    pThickClientDetail: '/projects/{projectPk}/thick-clients/{pk}/',
    pMobileAppList: '/projects/{projectPk}/mobile-applications/',
    pMobileAppDetail: '/projects/{projectPk}/mobile-applications/{pk}/',
    pServiceList: '/projects/{projectPk}/services/',
    pServiceDetail: '/projects/{projectPk}/services/{pk}/',
    pHostList: '/projects/{projectPk}/hosts/',
    pHostDetail: '/projects/{projectPk}/hosts/{pk}/',
    pWebAppList: '/projects/{projectPk}/web-applications/',
    pWebAppDetail: '/projects/{projectPk}/web-applications/{pk}/',

    // project checklists
    pChecklistList: '/projects/{projectPk}/checklists/',
    pChecklistDetail: '/projects/{projectPk}/checklists/{pk}/',
    pCheckCategoryList: '/projects/{projectPk}/checklist-categories/',
    pCheckCategoryDetail: '/projects/{projectPk}/checklist-categories/{pk}/',
    pCheckItemList: '/projects/{projectPk}/checklist-items/',
    pCheckItemDetail: '/projects/{projectPk}/checklist-items/{pk}/',

    // project reporting
    pReportDocumentList: '/projects/{pPk}/reports/{rPk}/report-releases/',
    pReportDocumentDetail: '/projects/{pPk}/reports/{rPk}/report-releases/{pk}/',
    pReportPreviewDocument: '/projects/{pPk}/reports/{rPk}/report-releases/preview_document/',
    pReportList: '/projects/{pPk}/reports/',
    pReportDetail: '/projects/{pPk}/reports/{pk}/',
    pReportVersionHistoryList: '/projects/{pPk}/reports/{rPk}/change-histories/',
    pReportVersionHistoryDetail: '/projects/{pPk}/reports/{rPk}/change-histories/{pk}/',

    pAccountList: '/projects/{projectPk}/accounts/',
    pAccountDetail: '/projects/{projectPk}/accounts/{pk}/',

    pVulnList: '/projects/{projectPk}/vulnerabilities/',
    pVulnDetail: '/projects/{projectPk}/vulnerabilities/{pk}/',

    pFindingList: '/projects/{pPk}/findings/',
    pFindingDetail: '/projects/{pPk}/findings/{pk}/',
    pFindingAsAdvisory: '/projects/{pPk}/findings/{pk}/as_advisory/',
    pFindingCopy: '/projects/{pPk}/findings/{pk}/copy/',
    pFindingAttachmentList: '/projects/{pPk}/findings/{fPk}/attachments/',
    pFindingAttachmentDetail: '/projects/{pPk}/findings/{fPk}/attachments/{pk}/',
    pFindingTimelineList: '/projects/{pPk}/findings/{fPk}/timelines/',
    pFindingTimelineDetail: '/projects/{pPk}/findings/{fPk}/timelines/{pk}/',
    pFindingCommentList: '/projects/{pPk}/findings/{fPk}/comments/',
    pFindingCommentDetail: '/projects/{pPk}/findings/{fPk}/comments/{pk}/',
    pFindingExportPdf: '/projects/{pPk}/findings/{pk}/export_pdf/',

    pFileList: '/projects/{pPk}/files/',
    pFileDetail: '/projects/{pPk}/files/{pk}/',
    pFileDownload: '/projects/{pPk}/files/{pk}/download/',

    pentestTypeList: '/pentest-types/',
    pentestTypeDetail: '/pentest-types/{pk}/',

    apiTokenList: '/api-tokens/',
    apiTokenDetail: '/api-tokens/{pk}/',

    // companies
    companyList: '/companies/',
    companyDetail: '/companies/{pk}/',
    cContactList: '/companies/{cPk}/contacts/',
    cContactDetail: '/companies/{cPk}/contacts/{pk}/',
    cInfoList: '/companies/{cPk}/information/',
    cInfoDetail: '/companies/{cPk}/information/{pk}',

    userUpdateProfile: '/users/update_profile/',
    userChangePassword: '/users/change_password/',
    userChangeEmail: '/users/change_email/',
    userChangeEmailConfirm: '/users/change_email_confirm/',
    userUserSettings: '/users/user-settings/',

    userList: '/users/',
    userDetail: '/users/{pk}/',

    groupList: '/groups/',

    technologyList: '/technologies/',
    technologyDetail: '/technologies/{pk}/',

    cweList: '/cwes/',
    cweDetail: '/cwes/{pk}/',

    vulnTemplateList: '/vulnerability-templates/',
    vulnTemplateDetail: '/vulnerability-templates/{pk}/',
    vulnTemplateTranslationList: '/vulnerability-templates/{vulnPk}/translations/',
    vulnTemplateTranslationDetail: '/vulnerability-templates/{vulnPk}/translations/{pk}/',

    // checklists
    checklistList: '/checks/checklists/',
    checklistDetail: '/checks/checklists/{pk}/',
    checkCategoryList: '/checks/categories/',
    checkCategoryDetail: '/checks/categories/{pk}/',
    checkItemList: '/checks/items/',
    checkItemDetail: '/checks/items/{pk}/',

    // advisories
    advisoryList: '/advisories/',
    advisoryDetail: '/advisories/{pk}/',

    aShareTokenList: '/advisories/{aPk}/share-tokens/',
    aShareTokenDetail: '/advisories/{aPk}/share-tokens/{pk}/',

    aStatTopVendors: '/advisories/statistics/top-vendors/',
    aStatTopProducts: '/advisories/statistics/top-products/',
    aStatTopVulns: '/advisories/statistics/top-vulnerabilities/',
    aStatTopSubmitters: '/advisories/statistics/top-submitters/',
    aStatBaseInfo: '/advisories/statistics/base-information/',

    aLabelList: '/advisory-labels/',
    aLabelDetail: '/advisory-labels/{pk}/',

    aAttachmentList: '/advisories/{aPk}/attachments/',
    aCommentList: '/advisories/{aPk}/comments/',
    aCommentDetail: '/advisories/{aPk}/comments/{pk}/',
    aTimelineList: '/advisories/{aPk}/timelines/',
    aTimelineDetail: '/advisories/{aPk}/timelines/{pk}/',
    aDownloadWithToken: '/advisories/{aPk}/download/{token}/',
    aDownloadPdf: '/advisories/{aPk}/export_pdf/',
    aPreview: '/advisories/{pk}/preview/',

    asProgramList: '/attack-surface/programs/',
    asProgramDetail: '/attack-surface/programs/{pk}/',
    asTagList: '/attack-surface/tags/',
    asTagDetail: '/attack-surface/tags/{pk}/',
    asTargetList: '/attack-surface/targets/',
    asTargetDetail: '/attack-surface/targets/{pk}/',
    asScanFindingList: '/attack-surface/scan-findings/',
    asScanFindingDetail: '/attack-surface/scan-findings/{pk}/',
    asUrlList: '/attack-surface/urls/',
    asUrlDetail: '/attack-surface/urls/{pk}/',
    asServiceList: '/attack-surface/services/',
    asServiceDetail: '/attack-surface/services/{pk}/',
    asServiceSearch: '/attack-surface/services/search/',
    asFindingList: '/attack-surface/findings/',
    asFindingDetail: '/attack-surface/findings/{pk}/',
    asFindingPdf: '/attack-surface/findings/{pk}/export_pdf/',
    asFindingImageList: '/attack-surface/finding-images/',
    asFindingComponentList: '/attack-surface/findings-components/',
    asFindingComponentDetail: '/attack-surface/findings-components/{pk}/',
    asScanList: '/attack-surface/scanning/scans/',
    asScanDetail: '/attack-surface/scanning/scans/{pk}/',
    asScannerList: '/attack-surface/scanning/scanners/',
    asScannerDetail: '/attack-surface/scanning/scanners/{pk}/',
    asScanTypeList: '/attack-surface/scanning/scan-types/',
    asScanTypeDetail: '/attack-surface/scanning/scan-types/{pk}/',

    // utils
    renderMarkdown: '/render-markdown/',
    cvss4Calc: '/cvss-calculator/4.0/',
    cvss3Calc: '/cvss-calculator/3.1/',

    // admin
    admSettingsGeneral: '/settings/general/',
    admSettingsDetail: '/settings/{pk}/',
    admSettingsAdvisories: '/settings/advisories/'
};

export default endpoints;
