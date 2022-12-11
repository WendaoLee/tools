<script setup>
/**
 * isShow:Boolean
 * categoryData:Object.
 */
import { useOneDefault } from '@/logic/dashboardapi'
import { isObjectEmpty } from '@/utils/fuc'
import { ref, watch } from 'vue'

let props = defineProps(['isLazy', 'isShow', 'categoryData'])
const emits = defineEmits(['onClosed'])

let { isGeometry, category, name } = props.categoryData
isGeometry = isGeometry?"(地物)":""
isGeometry = ref(isGeometry)
category = ref(category)
name = ref(name)

let isShow = ref(props.isShow)


let isHasSubType = ref(false)
let isHasDefaultAttribute = ref(false)

let renderDefaultAttributes = []
let renderPreferrence = []
let renderTypeDescriptArray = []
let renderDely = []
let default_data = useOneDefault().value[name.value]
console.log(default_data)

if (!isObjectEmpty(default_data)) {
    isHasDefaultAttribute.value = true
    console.log("default:",default_data.value)
    for (const key in default_data) {
        console.log(key)
        renderDefaultAttributes.push({
            "key": key,
            "type": default_data[key]["file_type"],
            "data": default_data[key]["file"]
        })
    }
}

for (const ele of category.value["specification"]) {
    renderTypeDescriptArray.push({
        "key": ele['keyName'],
        "type": ele['keyCategory']
    })
}

function onDialogClosed(){
    emits('onClosed')
}
</script>

<template>
    <el-dialog v-model="isShow" :title="`查看类型:${name}  ${isGeometry}`" @closed="onDialogClosed" width="50rem" height="200rem">
        <el-form style="width:100%;height:100%">
            <template v-if="isHasDefaultAttribute">
                <h3>{{ "默认属性:" }}</h3>
                <el-form-item v-for="ele in renderDefaultAttributes" :label="ele['key']" :key="ele.key">
                    <el-image v-if="ele['type'] == 'img'" :src="ele['data']" :fit="fill" style="width:30rem"></el-image>
                    <el-input v-else v-model="ele['data']" disabled>
                    </el-input>
                </el-form-item>
            </template>
            <template id="__OriginSpecification" v-if="true">
                <h3>{{ "定义:" }}</h3>
                <el-form-item v-for="renderOpts in renderTypeDescriptArray" :label="renderOpts['key']">
                    <el-input v-model="renderOpts['type']" disabled></el-input>
                </el-form-item>
            </template>
        </el-form>
    </el-dialog>
</template>