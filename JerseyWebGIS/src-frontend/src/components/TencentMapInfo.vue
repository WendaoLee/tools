<script setup>
import { TencentMap } from 'cutetencentmap'
import { useCategory } from '@/logic/dashboardapi'
import { getBatchedCategoryData } from '@/api/category'
import { ref, onMounted, watch, computed } from 'vue'
import { Literal_TMap_LatLng } from 'cutetencentmap/LiteralTencentMapClass'
import { ElMessage } from 'element-plus'
import CategoryPointAddTable from './CategoryPointAddTable.vue'

const { category_table, category } = useCategory()
console.log('category_table:', category_table)

const geometryCategory = ref({
    arr: []
})

const mapInstance = new TencentMap({
    theKey: "4GABZ-7B2W6-DEOSD-ERS4U-HEY5K-7BBQ6",
    isInit: true,
    rootElement: 'mapContainer1'
})
mapInstance._isMapInit(mapInstance._defaultMapSet)

const geometryRef = ref({})
const isInfoTableShow = ref(false)
const targetInfoTableData = ref({})
const targetInfoCategory = ref('')

function showInfoTable(category) {
    return function (evt) {
        console.log(evt)

        let pattern_lat = evt.latLng.lat
        let pattern_lng = evt.latLng.lng
        let pattern_id = evt.geometry.id
        console.log('he:', category)
        console.log('pattern lat,lng,id:', pattern_lat, pattern_lng, pattern_id)

        let pattern_matched = null
        for (let i = 0; i < geometryRef.value[category].length; i++) {
            let p = geometryRef.value[category][i]
            console.log('target p:', p['_Latitude'])
            if (p['_id'] == pattern_id) {
                console.log('pattern match:', p)
                pattern_matched = {}
                Object.assign(pattern_matched, p)
                console.log('pattern-value:', pattern_matched)
                break
            }
        }

        if (pattern_matched == null) {
            ElMessage({
                type: 'warning',
                message: '无法寻找到匹配的点数据'
            })
        } else {
            targetInfoTableData.value = pattern_matched
            targetInfoCategory.value = category
            isInfoTableShow.value = true
        }
    }
}

if (category_table.value.length == 0) {
    watch(category_table, () => {
        geometryCategory.value.arr = category_table.value.filter(ele => ele['isGeometry'])
        //此处获取的是范畴数据
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
                            position: Literal_TMap_LatLng(
                                ele['_Latitude'], ele['_Longitude']
                            )
                        }
                    })

                    geometryRef.value[key] = response[key]

                    mapInstance.BuildNewMultiMarker(key, {
                        zIndex: 1,
                        geometries: geo
                    })
                    setTimeout(() => {
                        mapInstance.multiMarkerLayer[key].layer.on('click', showInfoTable(key))
                    }, 5000)

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
        }).then(
            () => {

            }
        )
    })
}
else {
    geometryCategory.value.arr = category_table.value.filter(ele => ele['isGeometry'])
    //此处获取的是范畴数据
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
                        position: Literal_TMap_LatLng(
                            ele['_Latitude'], ele['_Longitude']
                        )
                    }
                })

                geometryRef.value[key] = response[key]

                mapInstance.BuildNewMultiMarker(key, {
                    zIndex: 1,
                    geometries: geo
                })
                setTimeout(() => {
                    mapInstance.multiMarkerLayer[key].layer.on('click', showInfoTable(key))
                }, 5000)

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
    }).then(
        () => {

        }
    )
}




</script>

<template>
    <div id="themapInfo">
        <CategoryPointAddTable @onClosed="isInfoTableShow = false" v-if="isInfoTableShow" :isShow="isInfoTableShow"
            :categoryData="category[targetInfoCategory]" :theId="targetInfoTableData['_id']"></CategoryPointAddTable>

        <div id="mapContainer1" style="width:100%;height:100%">
        </div>
    </div>

</template>