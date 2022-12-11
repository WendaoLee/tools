import request from '@/utils/request'

export function getCategory(){
    return request({
        'url':'/category',
        'method':'get'
    })
}

export function addCategory(categoryPostBody){
    return request({
        'url':'/category',
        'method':'post',
        'data':categoryPostBody
    })
}

export function getSingleCategoryData(queryPostBody){
    return request({
        'url':'/data/query',
        'method':'post',
        'data':queryPostBody
    })
}

export function getBatchedCategoryData(queryPostBody){
    return request({
        'url':'/data/batch',
        'method':'post',
        'data':queryPostBody
    })
}

export function addDefault(defaultPostBody){
    return request({
        'url':'/data',
        'method':'post',
        'data':defaultPostBody
    })
}

export function addData(postBody){
    return request({
        'url':'/data',
        'method':'post',
        'data':postBody
    })
}

