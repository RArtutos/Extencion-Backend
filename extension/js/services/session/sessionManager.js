import { storage } from '../../utils/storage.js';
import { cookieManager } from '../../utils/cookie/cookieManager.js';
import { sessionApi } from '../api/sessionApi.js';
import { sessionValidator } from './sessionValidator.js';
import { sessionTracker } from './sessionTracker.js';
import { analyticsService } from '../analyticsService.js';

export class SessionManager {
  constructor() {
    this.validator = sessionValidator;
    this.tracker = sessionTracker;
  }

  async startSession(accountId, domain) {
    try {
      // Validar límites
      if (!await this.validator.canStartSession(accountId)) {
        throw new Error('Maximum concurrent users reached');
      }

      // Iniciar sesión
      await sessionApi.startSession(accountId, domain);
      
      // Iniciar tracking
      this.tracker.startTracking();
      
      // Registrar analíticas
      await analyticsService.trackSessionStart(accountId, domain);
      
      return true;
    } catch (error) {
      console.error('Error starting session:', error);
      throw error;
    }
  }

  async endSession(accountId) {
    try {
      const currentAccount = await storage.get('currentAccount');
      if (!currentAccount || currentAccount.id !== accountId) return false;

      const domain = this.getAccountDomain(currentAccount);
      
      // Finalizar sesión en backend
      await sessionApi.endSession(accountId, domain);
      
      // Detener tracking
      this.tracker.stopTracking();
      
      // Registrar analíticas
      await analyticsService.trackSessionEnd(accountId, domain);
      
      return true;
    } catch (error) {
      console.error('Error ending session:', error);
      return false;
    }
  }

  async cleanupCurrentSession() {
    try {
      const currentAccount = await storage.get('currentAccount');
      if (!currentAccount) return;

      // Finalizar sesión
      await this.endSession(currentAccount.id);
      
      // Limpiar cookies
      await cookieManager.removeAccountCookies(currentAccount);
      
      // Limpiar storage
      await storage.remove('currentAccount');
      
    } catch (error) {
      console.error('Error cleaning up session:', error);
    }
  }

  getAccountDomain(account) {
    if (!account?.cookies?.length) return '';
    const domain = account.cookies[0].domain;
    return domain.startsWith('.') ? domain.substring(1) : domain;
  }
}

export const sessionManager = new SessionManager();