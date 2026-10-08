import { initializeApp, getApps, getApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';
import { getMessaging, isSupported } from 'firebase/messaging';

// Safely load AI Studio config if it exists (avoids build errors in other environments)
const modules = import.meta.glob('../firebase-applet-config.json', { eager: true });
const aiStudioConfigModule = modules['../firebase-applet-config.json'] as any;
const aiStudioConfig = aiStudioConfigModule?.default || aiStudioConfigModule || null;

const envConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

const activeConfig = aiStudioConfig || envConfig;
const databaseId = aiStudioConfig ? (aiStudioConfig.firestoreDatabaseId || '(default)') : '(default)';

// Initialize Firebase only if not already initialized
const app = getApps().length > 0 ? getApp() : initializeApp(activeConfig);

export const auth = getAuth(app);
export const db = getFirestore(app, databaseId);

export let messaging: any = null;
isSupported().then((supported) => {
  if (supported) {
    messaging = getMessaging(app);
  }
});

export const storage = getStorage(app);
