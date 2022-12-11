import axios from 'axios';
import {DEV_SERVER_PORT,DEV_SERVER_URL} from '@/assets/envir'

const httpservices = axios.create({
    baseURL:"http://"+DEV_SERVER_URL + ":" + DEV_SERVER_PORT,
    headers:{
        "Content-Type":"application/json"
    }
})

httpservices.interceptors.response.use(
    response=>{
        return response.data
    },
    function(error){
        console.error(
            error
        )
        return null
    }
)


export default httpservices
