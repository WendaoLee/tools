<script setup>
import { TencentMap } from 'cutetencentmap'
import { Literal_PointGeometry } from 'cutetencentmap/LiteralTencentMapClass'
import { ref, onMounted, watch, computed, getCurrentInstance } from 'vue'
import { useCategory } from '@/logic/dashboardapi'
import { getBatchedCategoryData, addData } from '@/api/category'
import { ElMessage } from 'element-plus'
import { random } from 'lodash'
import { TMap_LatLng } from 'cutetencentmap/TencentMapClass'

const { category_table } = useCategory()
console.log('category_table:', category_table)
console.log('category_table_data:', category_table.value)

let mapInstance = new TencentMap({
    theKey: "4GABZ-7B2W6-DEOSD-ERS4U-HEY5K-7BBQ6",
    isInit: true,
    rootElement: 'mapContainer'
})
mapInstance._isMapInit(mapInstance._defaultMapSet)

// if (mapInstance.instance == undefined) {
//             console.log('hook works!')
//             mapInstance._isMapInit(mapInstance._defaultMapSet)
//         }
// onMounted(() => {
//     console.log("onmounted")
//     console.log(document.getElementById('mapContainer'))
//     mapInstance = new TencentMap({
//         theKey: "4GABZ-7B2W6-DEOSD-ERS4U-HEY5K-7BBQ6",
//         isInit: true,
//         rootElement: 'mapContainer'
//     })

//     console.log(mapInstance)
// })

let targetMarker = null

const geometryCategory = ref({
    arr: []
})

const isStartAdded = ref(false)


if (category_table.value.length == 0) {
    watch(category_table, () => {
        geometryCategory.value.arr = category_table.value.filter(ele => ele['isGeometry'])
        getBatchedCategoryData(
            geometryCategory.value.arr.map(ele => {
                return {
                    category: ele['name'],
                    num: -1
                }
            })
        ).then(response => {
            console.log('getBateched:', response)
            for (const key in response) {
                if (response[key].length != 0) {
                    console.log('batched not 0:', key, response[key])
                    let geo = response[key].map(ele => {
                        return {
                            id: ele['_id'],
                            position: TMap_LatLng(
                                ele['_Latitude'], ele['_Longitude']
                            )
                        }
                    })

                    mapInstance.BuildNewMultiMarker(key, {
                        zIndex: 1,
                        geometries: geo
                    })

                    // mapInstance.value.BuildNewMultiMarker(key,{
                    //     geometries=
                    // })
                }
                else {
                    console.log('batched 0:', key)
                    mapInstance.BuildNewMultiMarker(key, {
                        zIndex: 1
                    })
                }
            }
        })
    })
}
else{
    geometryCategory.value.arr = category_table.value.filter(ele => ele['isGeometry'])
        getBatchedCategoryData(
            geometryCategory.value.arr.map(ele => {
                return {
                    category: ele['name'],
                    num: -1
                }
            })
        ).then(response => {
            console.log('getBateched:', response)
            for (const key in response) {
                if (response[key].length != 0) {
                    console.log('batched not 0:', key, response[key])
                    let geo = response[key].map(ele => {
                        return {
                            id: ele['_id'],
                            position: TMap_LatLng(
                                ele['_Latitude'], ele['_Longitude']
                            )
                        }
                    })

                    mapInstance.BuildNewMultiMarker(key, {
                        zIndex: 1,
                        geometries: geo
                    })

                    // mapInstance.value.BuildNewMultiMarker(key,{
                    //     geometries=
                    // })
                }
                else {
                    console.log('batched 0:', key)
                    mapInstance.BuildNewMultiMarker(key, {
                        zIndex: 1
                    })
                }
            }
        })
}


console.log('geometry:', geometryCategory)


function listner_addPoint(evt) {
    console.log('click event:', evt)
    console.log(mapInstance.multiMarkerLayer)
    targetMarker = mapInstance.multiMarkerLayer[targetType.value].layer
    targetMarker.add({
        position: evt.latLng
    })
}

function startAddPoint() {
    isStartAdded.value = true
    mapInstance.on('click', listner_addPoint)
}

function stopAddPoint() {
    isStartAdded.value = false
    mapInstance.off('click', listner_addPoint)
    console.log('geo:', mapInstance.multiMarkerLayer[targetType.value].layer.getGeometries())
    let temp = mapInstance.multiMarkerLayer[targetType.value].layer.getGeometries()
    let target_results_data = temp.map((ele) => {
        return {
            '_Latitude': ele['position']['lat'],
            '_Longitude': ele['position']['lng'],
            '_id': new Date().getMilliseconds() + random(10)
        }
    })
    console.log('submit_geo', target_results_data)
    addData(
        [
            {
                name: targetType.value,
                data: target_results_data
            }
        ]
    ).then(
        respose => {
            if (respose == 'Success') {
                ElMessage({
                    message: '添加点物成功！',
                    type: 'success'
                })
            }
            else {
                ElMessage({
                    message: 'error occurs',
                    type: 'error'
                })
            }
        }
    )

}

// mapInstance.value.on('click', (e) => {
//     console.log(e)
//     mapInstance.value.BuildNewMultiMarker("test")
// })

const targetType = ref('')

const isTypeSelect = computed(() => {
    return (targetType.value == '')
})

</script>
  
<template>
    <div id="tencentMapadd">
        <el-form title="Hello">
            <el-form-item label="选择添加的地物">
                <el-select v-model="targetType">
                    <el-option v-for="item in geometryCategory.arr" :key="item['name']" :label="item['name']"
                        :value="item['name']" />
                </el-select>
                <el-button type="success" :disabled="isStartAdded == false && isTypeSelect == true"
                    @click="startAddPoint">开始添加</el-button>
                <el-button type="danger" :disabled="!isStartAdded" @click="stopAddPoint">停止添加</el-button>
            </el-form-item>
        </el-form>
        <div id="mapContainer">
        </div>
    </div>
</template>