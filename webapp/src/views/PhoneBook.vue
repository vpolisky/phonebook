<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-container grid-list-md>
    <v-layout row wrap>

      <v-flex xs12 md4>
        <v-text-field label="Filter by name" v-model="name"></v-text-field>
      </v-flex>
      <v-flex xs12 md4>
        <v-text-field label="Filter by phone number" v-model="phone"></v-text-field>
      </v-flex>
      <v-flex xs12 md4>
        <v-text-field label="Filter by address" v-model="address"></v-text-field>
      </v-flex>

    </v-layout>

    <v-layout justify-end class="text-xs-right">
      <v-flex xs12 md4>
        <v-btn @click="getData(query)">Filter</v-btn>
      </v-flex>
    </v-layout>

    <v-layout row wrap>
      <v-flex xs12 v-if="loading">
        <v-progress-circular
          :size="50"
          color="primary"
          indeterminate
        ></v-progress-circular>
      </v-flex>
      <v-flex v-if="contacts">
        <v-data-table
          :headers="headers"
          :items="contacts"
          class="elevation-1"
          hide-actions
          :loading="loading"
        >
          <template v-slot:items="props">
            <td class="text-xs-right">{{ props.item.name }}</td>
            <td class="text-xs-right">{{ props.item.phone_number }}</td>
            <td class="text-xs-right">{{ props.item.address }}</td>
          </template>
        </v-data-table>
      </v-flex>
      <v-flex v-if="error" class="error elevation-4">
        An error occurred: Unable to fetch data
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  const axios = require('axios');

  export default {
    name: "PhoneBook",
    created() {
      this.getData()
    },
    data() {
      return {
        loading: false,
        contacts: null,
        error: false,
        headers: [
          {text: 'Name', value: 'name', align: 'right'},
          {text: 'Phone number', value: 'phone_number', align: 'right'},
          {text: 'Address', value: 'address', align: 'right'},
        ],
        name: null,
        phone: null,
        address: null
      }
    },
    computed: {
      query() {
        return {
          name: this.name,
          phone: this.phone,
          address: this.address,
        }
      }
    },
    methods: {
      getData(query) {
        this.loading = true
        axios.get('/api/phones/', {params: this.query})
          .then(res => {
            this.contacts = res.data
            this.error = false
          })
          .catch(err => {
            this.contacts = null
            this.error = true
          })
          .then(() => (this.loading = false))
      }
    }
  }
</script>

<style scoped>
  .error {
    border: red solid 1px;
    border-radius: 4px;
    padding: 1rem;
    color: darkred;
  }
</style>
