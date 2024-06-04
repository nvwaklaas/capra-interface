import { createApp} from 'vue'
import './style.css'
import App from './App.vue'

import FlashMessage from './components/FlashMessage.vue';

const app = createApp(App)

app.component('FlashMessage', FlashMessage)
app.mount('#app')
