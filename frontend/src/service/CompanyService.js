import { api } from '@/plugins/axios';

export default class CompanyService {
    getCompanies(params) {
        let url = '/companies/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    search(query) {
        let url = '/companies/';
        let config = { params: { search: query } };
        return api.get(url, config);
    }

    getCompany(companyId) {
        let url = '/companies/' + companyId + '/';
        return api.get(url);
    }

    deleteCompany(api, id) {
        let url = `/companies/${id}/`;
        return api.delete(url);
    }

    createCompany(api, data) {
        let url = '/companies/';
        return api.post(url, data);
    }

    patchCompany(api, companyId, data) {
        let url = '/companies/' + companyId + '/';
        return api.patch(url, data);
    }

    getCompanyInformation(companyId) {
        let url = '/companies/' + companyId + '/information/';
        return api.get(url);
    }

    createCompanyInformation(api, companyId, data) {
        let url = '/companies/' + companyId + '/information/';
        return api.post(url, data);
    }

    patchCompanyInformation(api, companyId, infoId, data) {
        let url = `/companies/${companyId}/information/${infoId}/`;
        return api.patch(url, data);
    }

    deleteCompanyInformation(api, companyId, id) {
        let url = '/companies/' + companyId + '/information/' + id + '/';
        return api.delete(url);
    }

    getContacts(companyId, params) {
        let url = '/companies/' + companyId + '/contacts/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createContact(api, companyId, data) {
        let url = '/companies/' + companyId + '/contacts/';
        return api.post(url, data);
    }

    deleteContact(api, companyId, contactId) {
        let url = '/companies/' + companyId + '/contacts/' + contactId + '/';
        return api.delete(url);
    }

    patchContact(api, companyId, contactId, data) {
        let url = `/companies/${companyId}/contacts/${contactId}/`;
        return api.patch(url, data);
    }

    uploadCompanyLogo(api, companyId, logo) {
        let url = '/companies/' + companyId + '/';
        let data = new FormData();
        data.append('logo', logo);
        return api.patch(url, data);
    }
}
