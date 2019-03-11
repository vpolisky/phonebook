import Vue from 'vue';
import Router from 'vue-router';
import PhoneBook from './views/PhoneBook.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'phonebook',
      component: PhoneBook,
    },
  ],
});
