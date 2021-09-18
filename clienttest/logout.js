const axios = require('axios')

async function logoutuser(){

const username = 'vt@gmail.com'
const password = 'test'

const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64')

const url = 'http://localhost:8000/api/session'

const response = await axios.delete(url, {
  headers: {
    'Authorization': `Basic ${token}`
  },
})

console.log(response.data)

}

logoutuser()