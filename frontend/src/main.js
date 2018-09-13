import Vue from 'vue'
import App from './App.vue'
import VueSocketIO from 'vue-socket.io';

Vue.use(VueSocketIO, 'http://localhost:5000');

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')
