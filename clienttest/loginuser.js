const axios = require('axios')

async function loginuser(){

const username = 'vkt@gmail.com'
const password = 'test'

const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64')

const url = 'http://3.93.69.236:8000/api/session'

const response = await axios.get(url, {
  headers: {
    'Authorization': `Basic ${token}`
  },
})

console.log(response.data)

}

loginuser()