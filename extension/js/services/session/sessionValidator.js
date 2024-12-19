import { sessionApi } from '../api/sessionApi.js';

export class SessionValidator {
  async validateSession(accountId) {
    const sessionStatus = await sessionApi.getSessionStatus(accountId);
    
    if (!sessionStatus.active_session) {
      if (sessionStatus.active_sessions >= sessionStatus.max_concurrent_users) {
        throw new Error('Session limit reached');
      }
    }
    
    return sessionStatus;
  }

  async canStartSession(accountId) {
    const sessionStatus = await sessionApi.getSessionStatus(accountId);
    return sessionStatus.active_sessions < sessionStatus.max_concurrent_users;
  }
}

export const sessionValidator = new SessionValidator();