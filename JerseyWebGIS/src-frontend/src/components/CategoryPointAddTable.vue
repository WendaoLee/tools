<script setup>
/**
 * isShow:Boolean
 * categoryData:Object.
 */
import { getSingleCategoryData,addData } from '@/api/category'
import { useOneDefault } from '@/logic/dashboardapi'
import { isObjectEmpty } from '@/utils/fuc'
import { ElMessage } from 'element-plus';
import { ref, watch, computed } from 'vue'

let props = defineProps(['isLazy', 'isShow', 'categoryData', 'theId'])
const emits = defineEmits(['onClosed'])

const enums = ref({
    type: [
        { label: "文本", value: 'Text' },
        { label: "数字", value: 'Double' },
        { label: "布尔", value: 'Boolean' },
        { label: "日期", value: 'Date' },
        { label: "时间", value: 'Time' },
        { label: "日期时间", value: 'Datetime' },
        { label: "图片", value: 'Binary' },
    ],
    bool: [
        { label: 'True', value: true },
        { label: 'False', value: false }
    ]
})

let { isGeometry, category, name } = props.categoryData
isGeometry = isGeometry ? "(地物)" : ""
isGeometry = ref(isGeometry)
category = ref(category)
name = ref(name)

let isShow = ref(props.isShow)

function unfolderSpec(arr) {
    let result_keys = []
    for (const ob of arr) {
        if (ob.keyName != "_Latitude" && ob.keyName != "_Longitude") {
            result_keys.push(ob.keyName)
        }
    }
    return result_keys
}

function createCategoryRef(arr) {
    let ref = {}
    for (const ob of arr) {
        ref[ob.keyName] = ob.keyCategory
    }
    return ref
}

let specs_keys = ref(unfolderSpec(category.value.specification))
let ori_specs_keys = ref(unfolderSpec(category.value.specification))
let defualt_keys = ref([])
let default_data = ref({})
let table_view_data = ref([])

let ref_category_type = ref(createCategoryRef(category.value.specification))

getSingleCategoryData({
    "category": "Default",
    "query": {
        "category": name.value
    }
}).then(
    response => {
        console.log('response', response)
        default_data.value = response
        for (let i = 0; i < response.length; i++) {
            if (response[i].categoryKey in specs_keys.value) {
                specs_keys.value.splice(i, 1)
                ori_specs_keys.value.splice(i, 1)
                defualt_keys.value.push(response[i].categoryKey)
            }
            default_data.value[response[i].categoryKey] = response[i]
        }

        if (!isObjectEmpty(default_data)) {
            isHasDefaultAttribute.value = true
            console.log("default:", default_data.value)
            for (const ob of default_data.value) {
                console.log(ob)
                console.log(default_data.value)
                renderDefaultAttributes.push({
                    "key": ob['categoryKey'],
                    "type": ob["file_type"],
                    "data": ob["file"]
                })
            }
        }

        for (const key of ori_specs_keys.value) {
            submitData.value[key] = null
        }

        getSingleCategoryData({
            "category": name.value,
            "query": {
                "_id": props.theId
            }
        }).then(
            response => {
                table_view_data.value = response
                submitData.value['_Latitude'] = response[0]['_Latitude']
                submitData.value['_Longitude'] = response[0]['_Longitude']
                submitData.value['_id'] = props.theId
            }
        )
    }
)


let isHasSubType = ref(false)
let isHasDefaultAttribute = ref(false)

const isAddNewVal = ref(false)
const submitData = ref({
})

let renderDefaultAttributes = []
let renderPreferrence = []
let renderTypeDescriptArray = []
let renderDely = []
// let default_data = useOneDefault().value[name.value]
console.log(default_data)

// if (!isObjectEmpty(default_data)) {
//     isHasDefaultAttribute.value = true
//     console.log("default:",default_data.value)
//     for (const key in default_data) {
//         console.log(key)
//         renderDefaultAttributes.push({
//             "key": key,
//             "type": default_data[key]["file_type"],
//             "data": default_data[key]["file"]
//         })
//     }
// }

// for (const ele of category.value["specification"]) {
//     renderTypeDescriptArray.push({
//         "key": ele['keyName'],
//         "type": ele['keyCategory']
//     })
// }

function onDialogClosed() {
    emits('onClosed')
}

const handleRequest = function (ref) {
    return (e) => {
        const fd = new FileReader()
        console.log(e)
        fd.readAsDataURL(e.file)
        fd.onload = () => {
            ref.value = fd.result
        }
    }
}

function handleFileRemove(ref) {
    return (e) => {
        console.log(e)
        ref.value = ''
    }
}

function submitNewData(){
    addData(
        [
            {
                name:name.value,
                data:[
                    submitData.value
                ]
            }
        ]
    ).then(
        response =>{
            ElMessage({
                type:'success',
                message:'提交成功!'
            })
            console.log(response)
            isAddNewVal.value =false
        }
    )
}

</script>

<template>
    <el-dialog v-model="isShow" :title="`查看类型:${name}  ${isGeometry}`" @closed="onDialogClosed" width="50rem"
        height="200rem">
        <el-form style="width:100%;height:100%">
            <template v-if="isHasDefaultAttribute">
                <h3>{{ "默认属性:" }}</h3>
                <el-form-item v-for="ele in renderDefaultAttributes" :label="ele.key" :key="ele.key">
                    <el-image v-if="ele['type'] == 'img'" :src="ele['data']" :fit="fill" style="width:30rem"></el-image>
                    <el-input v-else v-model="ele['data']" disabled>
                    </el-input>
                </el-form-item>
            </template>
            <template id="__OriginSpecification" v-if="true">
                <h3>{{ "该点属性值：" }}</h3>
                <!-- <el-form-item v-for="key in specs_keys" :label="key">
                    <el-input v-model="renderOpts['type']" disabled></el-input>
                </el-form-item> -->

                <el-form-item>
                    <el-table :data="table_view_data">
                        <el-table-column v-for="key in specs_keys" :prop="key" :label="key"></el-table-column>
                    </el-table>
                </el-form-item>

                <!-- <el-form-item v-for="number in specs_keys.length">
                    <el-form-item :label="specs_keys[number-1]">
                        <el-upload v-if="attributeData[number - 1].keyCategory == 'Binary'" action=""
                            :http-request="handleRequest(number)" :on-remove="handleFileRemove(number)"
                            list-type="picture" limit=1>
                            <i v-if="!attributeData[number - 1].keyDefault">点击此处上传图片</i>
                        </el-upload>
                        <el-input v-else-if="attributeData[number - 1].keyCategory == 'Text'"
                            v-model="attributeData[number - 1].keyDefault"></el-input>
                        <el-input-number v-else-if="attributeData[number - 1].keyCategory == 'Double'"
                            v-model="attributeData[number - 1].keyDefault"></el-input-number>
                        <el-date-picker v-else-if="attributeData[number - 1].keyCategory == 'Date'"
                            v-model="attributeData[number - 1].keyDefault"></el-date-picker>
                        <el-date-picker type="time" v-else-if="attributeData[number - 1].keyCategory == 'Time'"
                            v-model="attributeData[number - 1].keyDefault"></el-date-picker>
                        <el-date-picker type="datetime" v-else-if="attributeData[number - 1].keyCategory == 'Datetime'"
                            v-model="attributeData[number - 1].keyDefault"></el-date-picker>
                        <el-select v-else-if="attributeData[number - 1].keyCategory == 'Boolean'"
                            v-model="attributeData[number - 1].keyDefault">
                            <el-option v-for="item in enums.bool" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="danger" style="margin-left: 90%;" @click="deleteAttribute(number)">
                            删除
                        </el-button>
                    </el-form-item>
                </el-form-item> -->
            </template>
        </el-form>
        <template #footer>
            <el-button type="success" @click="isAddNewVal = true">添加新的属性记录</el-button>
        </template>
    </el-dialog>
    <el-dialog v-model="isAddNewVal" @closed="isAddNewVal = false" title="添加新的属性记录">
        <el-form>
            <el-form-item v-for="key in specs_keys">
                    <el-form-item :label="key">
                        <el-upload v-if="ref_category_type[key] == 'Binary'" action=""
                            :http-request="handleRequest(submitData[key])" :on-remove="handleFileRemove(submitData[key])"
                            list-type="picture" limit=1>
                            <i v-if="!submitData[key]">点击此处上传图片</i>
                        </el-upload>
                        <el-input v-else-if="ref_category_type[key] == 'Text'"
                            v-model="submitData[key]"></el-input>
                        <el-input-number v-else-if="ref_category_type[key] == 'Double'"
                            v-model="submitData[key]"></el-input-number>
                        <el-date-picker v-else-if="ref_category_type[key] == 'Date'"
                            v-model="submitData[key]"></el-date-picker>
                        <el-date-picker type="time" v-else-if="ref_category_type[key] == 'Time'"
                            v-model="submitData[key]"></el-date-picker>
                        <el-date-picker type="datetime" v-else-if="ref_category_type[key] == 'Datetime'"
                            v-model="submitData[key]"></el-date-picker>
                        <el-select v-else-if="ref_category_type[key] == 'Boolean'"
                            v-model="submitData[key]">
                            <el-option v-for="item in enums.bool" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                        <el-input v-else v-model="submitData[key]"></el-input>
                    </el-form-item>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button type="success" @click="submitNewData">提交</el-button>
        </template>
    </el-dialog>
</template>