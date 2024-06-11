import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getMessaging, getToken, onMessage } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-messaging.js";

const firebaseConfig = {
    apiKey: "AIzaSyAw_jsdPCw4zYVs9SVKj_V0S8yA88dZ7SE",
    authDomain: "cryptoapp-a71a5.firebaseapp.com",
    projectId: "cryptoapp-a71a5",
    storageBucket: "cryptoapp-a71a5.appspot.com",
    messagingSenderId: "1035793599455",
    appId: "1:1035793599455:web:999edd3e2c10af157b126a",
    measurementId: "G-E99FTKLEGL"
  };

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

export { messaging, getToken, onMessage };

