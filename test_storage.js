import { initializeApp } from 'firebase/app';
import { getStorage, ref, uploadString } from 'firebase/storage';
import fs from 'fs';

const aiStudioConfig = JSON.parse(fs.readFileSync('firebase-applet-config.json', 'utf8'));

const app = initializeApp({
  projectId: aiStudioConfig.projectId,
  appId: aiStudioConfig.appId,
  apiKey: aiStudioConfig.apiKey,
  storageBucket: aiStudioConfig.storageBucket
});

const storage = getStorage(app);
const storageRef = ref(storage, 'test.txt');

uploadString(storageRef, 'Hello World').then(() => {
  console.log('Upload successful');
  process.exit(0);
}).catch((err) => {
  console.error('Upload failed:', err);
  process.exit(1);
});
