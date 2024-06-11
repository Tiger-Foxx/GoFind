import { messaging, getToken } from './firebase.js';

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('static/firebase-messaging-sw.js').then((registration) => {
        messaging.useServiceWorker(registration);

        function requestPermission() {
            alert('re');
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    getToken(messaging, { vapidKey: 'YOUR_VAPID_PUBLIC_KEY' }).then(currentToken => {
                        if (currentToken) {
                            console.log('FCM Token:', currentToken);
                            sendTokenToServer(currentToken);
                        } else {
                            console.log('No registration token available. Request permission to generate one.');
                        }
                    }).catch(err => {
                        console.log('An error occurred while retrieving token. ', err);
                    });
                } else {
                    console.log('Notification permission denied.');
                }
            });
        }

        function sendTokenToServer(token) {
            fetch('/update-fcm-token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ token: token }),
            }).then(response => response.json()).then(data => {
                console.log('Token sent to server successfully:', data);
            }).catch(error => {
                console.error('Error sending token to server:', error);
            });
        }

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        requestPermission();
    }).catch((err) => {
        console.log('Service worker registration failed, error:', err);
    });
}
