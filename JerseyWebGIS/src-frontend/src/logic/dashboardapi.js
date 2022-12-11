import { ref } from "vue";
import {getCategory,getSingleCategoryData} from '@/api/category'

let category = ref({})
let category_table = ref([])
let refarray_category = ref([])

let default_data = ref({})

export function ResetCategory(){
    getCategory().then(
        newlyCategories => {
            if(newlyCategories == null){
                return
            }
            let categoriesLen = newlyCategories.length
            let newlyCategory = {}
            let newlyCategoryTable = []
            let newlyRefArray_Category = []
            for(let i = 0;i < categoriesLen;i++){
                const NAME = newlyCategories[i]["name"]

                let DEFINIATION = newlyCategories[i]
                DEFINIATION['category'] = JSON.parse(DEFINIATION['category'].replaceAll('\'','\"'))

                newlyCategory[NAME] = DEFINIATION
                newlyRefArray_Category[i] = NAME
                newlyCategoryTable[i] = DEFINIATION
            }
            category.value = newlyCategory
            category_table.value = newlyCategoryTable
            refarray_category.value = newlyRefArray_Category 
        }
    )
}

export function ResetOneCategoryDefaultData(category){
    getSingleCategoryData({
        "category":"Default",
        "query":{
            "category":category
        }
    }).then(
        newlyDefault =>{
            if(newlyDefault == null){
                return
            }

            default_data.value[category] = {}
            
            for (const oneDefaultData of newlyDefault) {
                let {categoryKey,file,file_type} = oneDefaultData
                default_data.value[category][categoryKey] = {
                    "file":file,
                    "file_type":file_type
                }
                
            }
            console.log(default_data.value)
        }
    )
}

export function useCategory(){
    return {category,category_table,refarray_category}
}


export function useOneDefault(){
    return default_data
}
 