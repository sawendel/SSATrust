import { lastValueFrom } from 'rxjs';
import { ajax } from 'rxjs/ajax';

export const logger = {
  logEvent: async (uid, workflowId, eventType, templateName, templateType, metadata) => {
    return lastValueFrom(ajax({
      url: 'https://k1sx4sgipa.execute-api.us-east-2.amazonaws.com/prod/logs',
      crossDomain: true,
      method: 'POST',
      body: {
        userId: uid,
        metadata,
        eventType,
        workflowId,
        templateName,
        templateType,
      }
    }));
  }
};

export default logger;
