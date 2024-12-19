import { storage } from '../../utils/storage.js';
import { analyticsService } from '../analyticsService.js';
import { SESSION_CONFIG } from '../../config/constants.js';

export class SessionTracker {
  constructor() {
    this.pollInterval = null;
  }

  startTracking() {
    if (this.pollInterval) return;
    
    this.pollInterval = setInterval(async () => {
      await this.trackCurrentSession();
    }, SESSION_CONFIG.REFRESH_INTERVAL);
  }

  stopTracking() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
      this.pollInterval = null;
    }
  }

  async trackCurrentSession() {
    const currentAccount = await storage.get('currentAccount');
    if (!currentAccount) return;

    await analyticsService.trackPageView(window.location.hostname);
  }
}

export const sessionTracker = new SessionTracker();