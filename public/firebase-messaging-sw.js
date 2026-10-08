importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-messaging-compat.js');

firebase.initializeApp({
  projectId: "methodical-zephyr-0fs6l",
  appId: "1:218295279093:web:b5955ab091ad7d3fddd4bc",
  apiKey: "AIzaSyAUEClqA6lPa1tx9CPvJttgUD9xys4o1bM",
  authDomain: "methodical-zephyr-0fs6l.firebaseapp.com",
  messagingSenderId: "218295279093",
  storageBucket: "methodical-zephyr-0fs6l.firebasestorage.app",
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  
  if (payload.data && payload.data.type === 'silent_message') {
    const notificationTitle = payload.data.title || 'New message';
    const notificationOptions = {
      body: payload.data.body || '',
      icon: '/vite.svg',
      silent: true,
      data: payload.data
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
  }
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      // Check if there is already a window/tab open with the target URL
      for (let i = 0; i < windowClients.length; i++) {
        let client = windowClients[i];
        if (client.url.includes(self.registration.scope) && 'focus' in client) {
          return client.focus();
        }
      }
      // If not, then open the target URL in a new window/tab.
      if (clients.openWindow) {
        return clients.openWindow('/');
      }
    })
  );
});
