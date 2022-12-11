<script setup>
// import {getCategory} from '@/logic/dashboardapi'
import { ref } from 'vue';
import { ResetCategory, useCategory,ResetOneCategoryDefaultData } from '@/logic/dashboardapi'
import CategoryInfoTable from './CategoryInfoTable.vue';
import CategoryAddTable from './CategoryAddTable.vue'

let { category_table, category,refarray_category } = useCategory()

let isShowInfo = ref(false)
let isShowAddTable = ref(false)

let targetData = ref({
    'name': '',
    'category': {
        'name': '',
        'specification': []
    },
    'isGeometry': {}
})

ResetCategory()

function show(data) {
    isShowInfo.value = true
    targetData.value = data
    console.log(targetData.value)
}

function addData() {
    isShowAddTable.value = true
}

setTimeout(()=>{
    for (const iterator of refarray_category.value) {
        ResetOneCategoryDefaultData(iterator)
    }
},2000)

</script>

<template>
    <div id="categoryTable">
        <CategoryAddTable v-if="isShowAddTable" :isShow="isShowAddTable" @onClosed="isShowAddTable = false">
        </CategoryAddTable>

        <CategoryInfoTable v-if="isShowInfo" :isShow="isShowInfo" :categoryData="targetData"
            @onClosed="isShowInfo = false"></CategoryInfoTable>



        <el-table :data="category_table" border="true">
            <el-table-column prop="name" label="类型名"></el-table-column>
            <el-table-column prop="isGeometry" label="是否地物"></el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button type="primary" @click="show(scope.row)">
                        查看定义
                    </el-button>
                    <el-button type="danger">
                        删除类型
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-row justify="center">
            <el-button type="success" @click="addData">添加类型</el-button>
        </el-row>
    </div>

</template>