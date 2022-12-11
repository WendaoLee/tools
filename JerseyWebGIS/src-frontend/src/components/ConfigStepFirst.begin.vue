<script setup>
import { useConfigStepNext } from '@/logic/setupconfig'
import {ArrowRight} from '@element-plus/icons-vue'


</script>

<template>
    <div id="configBeginning">
    <div id="beginText">
        <el-row> <img src="@/assets/map.png" class="toBeCenter"></el-row>

        <el-row>
            <h1 id="header" class="toBeCenter">开始配置您的地图</h1>
        </el-row>
        <el-row>
            <h3 id="subheader" class="toBeCenter">Begin Installation</h3>
        </el-row>
        <el-row>
        <p id="description" class="toBeCenter" style="margin-top: .3rem;">JerseyWebGIS</p>
        </el-row>
        <el-row>
        <p id="description" class="toBeCenter">是一款快捷的WebGIS-PackTool</p>
        </el-row>
        <el-row>
        <p id="description" class="toBeCenter">通过以下设置步骤，您可以快速打包发布主要用于<b>地物数据</b>展示与采集的WebGIS服务</p>
        </el-row>
    </div>

    <div id="actionButton">
    <el-row><el-button type="success" size="large" class="toBeCenter" @click="useConfigStepNext"> 开始配置 <el-icon><ArrowRight></ArrowRight></el-icon></el-button></el-row>
    </div>
</div>
        

</template>

<style scoped>
.toBeCenter {
    margin:0 auto;
}

#header{
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

#actionButton{
    margin:2.5rem 25% 0 25%
}
</style>