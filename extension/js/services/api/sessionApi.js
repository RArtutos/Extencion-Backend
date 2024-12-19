import { httpClient } from '../../utils/httpClient.js';

export class SessionApi {
  async getSessionStatus(accountId) {
    return await httpClient.get(`/api/accounts/${accountId}/session`);
  }

  async startSession(accountId, domain) {
    return await httpClient.post('/api/sessions/start', {
      account_id: accountId,
      domain,
      timestamp: new Date().toISOString()
    });
  }

  async updateSession(accountId, domain) {
    return await httpClient.put(`/api/sessions/${accountId}`, {
      domain,
      timestamp: new Date().toISOString()
    });
  }

  async endSession(accountId, domain) {
    return await httpClient.post('/api/sessions/end', {
      account_id: accountId,
      domain,
      timestamp: new Date().toISOString()
    });
  }
}

export const sessionApi = new SessionApi();