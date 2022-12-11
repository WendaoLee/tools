/**
 * @module default
 * 保留类型（Category）Default的相关封装类型。
 */

export function getDefaultPostBody({file,file_type,category,categoryKey}){
    return {
        "file":file,
        "file_type":file_type,
        "category":category,
        "categoryKey":categoryKey
    }
}