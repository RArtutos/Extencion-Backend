import { SESSION_CONFIG } from '../config/constants.js';
import { storage } from '../utils/storage.js';
import { httpClient } from '../utils/httpClient.js';
import { cookieManager } from '../utils/cookie/cookieManager.js';
import { analyticsService } from './analyticsService.js';

export class SessionManager {
  constructor() {
    this.activeTimers = new Map();
    this.pollInterval = null;
    this.initializeSessionCleanup();
  }

  initializeSessionCleanup() {
    chrome.runtime.onSuspend.addListener(() => {
      this.cleanupCurrentSession();
    });
  }

  async startPolling() {
    if (this.pollInterval) return;
    
    this.pollInterval = setInterval(async () => {
      const currentAccount = await storage.get('currentAccount');
      if (currentAccount) {
        await this.updateSessionStatus(currentAccount.id);
      }
    }, SESSION_CONFIG.REFRESH_INTERVAL);
  }

  stopPolling() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
      this.pollInterval = null;
    }
  }

  async updateSessionStatus(accountId) {
    try {
      const response = await httpClient.get(`/api/sessions/${accountId}/status`);
      const currentAccount = await storage.get('currentAccount');
      
      if (!response.active_session && response.active_sessions >= response.max_concurrent_users) {
        await this.cleanupCurrentSession();
        throw new Error('Session limit reached');
      }

      if (currentAccount?.id === accountId) {
        await httpClient.put(`/api/sessions/${accountId}`, {
          domain: window.location.hostname,
          timestamp: new Date().toISOString()
        });
      }
      
      return response;
    } catch (error) {
      console.error('Error updating session status:', error);
      throw error;
    }
  }

  async startSession(accountId, domain) {
    try {
      const sessionInfo = await this.updateSessionStatus(accountId);
      if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
        throw new Error('Maximum concurrent users reached');
      }

      await httpClient.post('/api/sessions/start', {
        account_id: accountId,
        domain,
        timestamp: new Date().toISOString()
      });

      await analyticsService.trackSessionStart(accountId, domain);
      this.startPolling();
      return true;
    } catch (error) {
      console.error('Error starting session:', error);
      throw error;
    }
  }

  async endSession(accountId) {
    try {
      const currentAccount = await storage.get('currentAccount');
      if (currentAccount?.id === accountId) {
        const domain = this.getAccountDomain(currentAccount);
        
        await httpClient.post('/api/sessions/end', {
          account_id: accountId,
          domain,
          timestamp: new Date().toISOString()
        });

        await analyticsService.trackSessionEnd(accountId, domain);
        this.stopPolling();
      }
      return true;
    } catch (error) {
      console.error('Error ending session:', error);
      return false;
    }
  }

  async cleanupCurrentSession() {
    try {
      const currentAccount = await storage.get('currentAccount');
      if (currentAccount) {
        await this.endSession(currentAccount.id);
        await cookieManager.removeAccountCookies(currentAccount);
        await storage.remove('currentAccount');
      }
      
      this.stopPolling();
      this.clearAllTimers();
    } catch (error) {
      console.error('Error cleaning up session:', error);
    }
  }

  clearAllTimers() {
    this.activeTimers.forEach(timer => {
      if (timer) clearTimeout(timer);
    });
    this.activeTimers.clear();
  }

  getAccountDomain(account) {
    if (!account?.cookies?.length) return '';
    const domain = account.cookies[0].domain;
    return domain.startsWith('.') ? domain.substring(1) : domain;
  }
}

export const sessionManager = new SessionManager();