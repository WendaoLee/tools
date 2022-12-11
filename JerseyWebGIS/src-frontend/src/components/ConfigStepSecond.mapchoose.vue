<script setup>
import { useConfigStepNext, useConfigStepPre,useConfig } from '@/logic/setupconfig'
import { ArrowRight, ArrowLeft } from '@element-plus/icons-vue'

const config = useConfig()
const options = [
    { label: '腾讯地图', value: 'TencentMap' }
]
</script>

<template>
    <div id="configMapChoose">
    <div id="info">
        <el-row>
            <h1 id="header">选择地图框架</h1>
        </el-row>
        <el-row>
            <h3 id="subheader">MapEngie</h3>
        </el-row>
        <el-row>
            <p id="description" class="toBeCenter" style="margin-top: .3rem;">
                地图框架指的是您所要使用的渲染地图的地图容器，例如MapBox，OpenLayers，Leaflet。
                <br>
                由于时间与精力限制，出于便捷中国大陆用户使用的考虑，我们目前只封装了腾讯地图的使用。也许以后有精力会添加其他地图的使用。
            </p>
        </el-row>
    </div>

    <div id="component">
        <el-row>
        <el-form class="toBeCenter" style="margin-left: 25%;margin-right:auto;width:50%" size="large" label-position="left">
        <el-form-item label="选择地图框架">
            <el-select v-model="config.mapEngine" placeholder="选择一样地图框架" size="large">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>
        </el-form-item>
        <el-form-item v-if="config.mapEngine == 'TencentMap'" label="输入开发Key">
            <el-input style="margin-bottom: -0.4rem;" v-model="config.mapOptions.key" placeholder="在此输入您的腾讯地图开发者Key" />
            <p class="comment" style="margin-bottom: -1.2rem;">如果您不知道什么是开发者Key，请参阅<a href="https://lbs.qq.com/webApi/javascriptGL/glGuide/glBasic">腾讯地图官方文档</a>。
            </p>
            <p class="comment">同时，请确保该Key对应的应用有JavaScript APIv1的使用权限。</p>
        </el-form-item>
        </el-form>
        </el-row>
    </div>

    <div id="actionButton">
        <!-- <el-row justify="space-between">

            <el-col :span="20" :offset="1">
            <el-button type="danger" size="large" @click="useConfigStepNext">
                    <el-icon>
                        <ArrowLeft></ArrowLeft>
                    </el-icon> 上一步
            </el-button>
            </el-col>
                <el-col :span="3">
                    <el-button type="success" size="large" @click="useConfigStepNext">下一步 <el-icon>
                        <ArrowRight></ArrowRight>
                    </el-icon>
                </el-button>
                </el-col>
        </el-row> -->
        <el-row>
            <el-button-group class="toBeCenter">
                <el-button type="danger" size="large" @click="useConfigStepPre">
                    <el-icon>
                        <ArrowLeft></ArrowLeft>
                    </el-icon> 上一步
                </el-button>
                <el-button type="success" size="large" @click="useConfigStepNext">下一步 <el-icon>
                        <ArrowRight></ArrowRight>
                    </el-icon>
                </el-button>
            </el-button-group>
        </el-row>

    </div>
</div>
</template>

<style scoped>
.toBeCenter {
    margin: 0 auto;
}

.comment{
    font-size: .6rem;
    color: #476582;
    margin-block-start: 0;
    margin-block-end: 0;
}

#header {
    font-size: 1.5rem;
    color: #0B346E;
    margin-bottom: 0;
}

#subheader {
    font-size: 1.3rem;
    line-height: 1.2;
    margin-top: .25rem;
    color: #476582;
}

#description {
    font-size: 1rem;
    color: #476582;
}

#actionButton {
    margin-top: 2.5rem
}

#component {
    margin-top: 3rem;
    margin-right: auto;
}
</style>