const { initializeApp, cert } = require('firebase-admin/app');
const { getMessaging } = require('firebase-admin/messaging');
console.log(typeof initializeApp, typeof cert, typeof getMessaging);
