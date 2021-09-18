const axios = require('axios')

async function createuser(){

const username = 'vt@gmail.com'
const password = 'test'
const role = 'ADMIN'

const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64')

const url = 'http://localhost:8000/api/account'
const data = {
	"username": username,
	"password": password,
	"role": role
}

const response = await axios.post(url, data, {
  headers: {
    'Authorization': `Basic ${token}`
  },
})

console.log(response.data)

}

createuser()