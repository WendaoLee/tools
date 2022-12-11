import requests from '@/utils/request'

export function addDefault(){
    return requests({
        url:'/'
    })
}