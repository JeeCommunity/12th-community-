import { initializeApp, cert } from 'firebase-admin/app';
import { getFirestore } from 'firebase-admin/firestore';

const serviceAccountStr = process.env.VITE_FIREBASE_SERVICE_ACCOUNT_KEY;
if (serviceAccountStr) {
  const serviceAccount = JSON.parse(serviceAccountStr);
  initializeApp({
    credential: cert(serviceAccount)
  });
  const db = getFirestore();
  
  async function run() {
    const users = await db.collection('users').get();
    users.forEach(doc => {
      console.log(doc.id, doc.data());
    });
  }
  run().catch(console.error);
} else {
  console.log("No service account key found");
}
