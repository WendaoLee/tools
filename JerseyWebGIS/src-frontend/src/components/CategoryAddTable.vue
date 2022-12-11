<script setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { useCategory,ResetCategory } from '@/logic/dashboardapi'
import { addCategory, addDefault } from '@/api/category'
import { ElMessage } from 'element-plus'

let props = defineProps(['isShow'])
const emits = defineEmits(['onClosed'])
let { refarray_category } = useCategory()

let type_ref = refarray_category.value.map((ele) => {
    return {
        label: ele,
        value: ele
    }
})

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

enums.value["category"] = [...enums.value.type, ...type_ref]

/**
 * {
        keyName: "",
        keyCategory: "",
        keyDefault: "",
        keyDefaultType: ""
    }
 */
const attributeData = ref([

])

/**
 * {
        keyName: "",
        keyCategory: ""
    }
 */
const specificationData = ref([
])

const isHasPosition = ref(false)
const attributesNums = ref(attributeData.value.length)
const specNums = ref(specificationData.value.length)
const categoryName = ref('')

const targetDefault = ref(0)

function addCategorySpec() {
    specificationData.value.push({
        keyName: "",
        keyCategory: ""
    })
    specNums.value++
}

function deleteCategorySpec(nums) {
    specificationData.value.splice(nums - 1, 1)
    specNums.value--
}

function onDialogClosed() {
    emits('onClosed')
}

function addAttribute() {
    attributeData.value.push({
        keyName: "",
        keyCategory: "",
        keyDefault: null,
        keyDefaultType: ""
    })
    attributesNums.value++
}

function deleteAttribute(nums) {
    attributeData.value.splice(nums - 1, 1)
    attributesNums.value--
}

const handleRequest = function (nums) {
    targetDefault.value = nums
    return (e) => {
        const fd = new FileReader()
        console.log(e)
        fd.readAsDataURL(e.file)
        fd.onload = () => {
            attributeData.value[nums - 1].keyDefault = fd.result
            attributeData.value[nums - 1].keyDefaultType = e.file.type
        }
    }
}

function handleFileRemove(nums) {
    return (e) => {
        console.log(e)
        attributeData.value[nums - 1].keyDefault = ""
    }
}

function constructCategoryPost() {
    let defaultCategory = attributeData.value.map((ele) => {
        return {
            keyName: ele.keyName,
            keyCategory: ele.keyCategory
        }
    })
    
    let results_spec = [...specificationData.value.map((ele) => { return { keyName: ele.keyName, keyCategory: ele.keyCategory } }), ...defaultCategory]
    if(isHasPosition.value == true){
        results_spec.push({
            keyName:"_Latitude",
            keyCategory:"Double"
        })
        results_spec.push({
            keyName:"_Longitude",
            keyCategory:"Double"
        })
    }


    let results_category_name = categoryName.value
    let results_isGeometry = isHasPosition.value

    let results_default = attributeData.value.map((ele) => {
        let type = typeof (ele['keyDefault'])
        if (typeof (ele['keyDefault']) == 'string') {
            ele['keyDefault'].includes('data:') ? type = 'img' : type
        }
        return {
            "file": ele['keyDefault'],
            "file_type": type,
            "category": results_category_name,
            "categoryKey": ele["keyName"]
        }
    })



    ElMessage({
        message: '正在上传类型定义中...',
        type: 'warning'
    })
    addCategory(
        [
            {
                name: results_category_name,
                specification: results_spec,
                isGeometry: results_isGeometry
            }
        ]
    ).then(response => {

        if (response == "Success") {
            ElMessage({
                message: '类型定义上传成功',
                type: 'success'
            })
            ElMessage({
                message: '正在上传属性默认值',
                type: 'warning'
            })
            addDefault(
                [
                    {
                        name: "Default",
                        data: results_default
                    }
                ]
            ).then(response => {
                if (response == "Success") {
                    ElMessage({
                        message: '属性默认值上传成功',
                        type: 'success'
                    })
                    ResetCategory()
                    onDialogClosed()
                }
            })
            // onDialogClosed()
        }
    })
}

</script>

<template>
    <el-dialog title="定义一个新类型" @closed="onDialogClosed" v-model="props.isShow" style="width:80rem">
        <el-form>
            <el-form-item label="类型名：" width="100px">
                <el-input v-model="categoryName"></el-input>
            </el-form-item>
            <el-form-item>
                <el-checkbox size="large" label="是否是地物" v-model="isHasPosition"></el-checkbox>
            </el-form-item>
            <template v-if="isHasPosition">
                <h3>属性
                </h3>
                <h7>属性是一个地物存有的默认值。例如同一个树种，它们有同样的属性“树种名”。在此处即可为这样的属性添加默认值。</h7>

                <el-form-item v-for="number in attributesNums">
                    <el-form-item label="属性名:">
                        <el-input v-model="attributeData[number - 1].keyName"></el-input>
                    </el-form-item>
                    <el-form-item label="类型:">
                        <el-select v-model="attributeData[number - 1].keyCategory">
                            <el-option v-for="item in enums.type" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="值:">
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
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" style="margin-left: 90%;" @click="addAttribute">
                        点击添加
                    </el-button>
                </el-form-item>
            </template>
            <template v-if="true">
                <h3>类型定义</h3>
                <h7>在这里添加类型定义。如果您指定的类型为一个地物的话，它所定义的数据只能在最终发布的服务中添加。</h7>
                <el-form-item v-for="number in specNums">
                    <el-form-item label="键名：">
                        <el-input v-model="specificationData[number - 1].keyName"></el-input>
                    </el-form-item>
                    <el-form-item label="类型：">
                        <el-select v-model="specificationData[number - 1].keyCategory">
                            <el-option v-for="item in enums.category" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                    </el-form-item>
                    <el-button type="danger" style="margin-left: 5%;" @click="deleteCategorySpec(number)">
                        删除
                    </el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" style="margin-left: 90%;" @click="addCategorySpec">
                        添加类型定义
                    </el-button>
                </el-form-item>
            </template>
        </el-form>

        <template #footer>
            <el-button type="success" @click="constructCategoryPost()">提交</el-button>
        </template>
    </el-dialog>
</template>

