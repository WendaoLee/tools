<script setup>
import { useConfigStepPre, useConfigWithIsFinishConfig, mapOptions, dbOptions, protocolOptions, useConfigStepTo } from '@/logic/setupconfig'
import { ArrowLeft, Select, Warning,Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus';
import { useWebSocket } from '@/logic/websocket'
import { useRouter } from 'vue-router';

const { isConnectionOpened,websocketClient } = useWebSocket()
const { config, isFinishConfig } = useConfigWithIsFinishConfig()

const router = useRouter()

function commitConfig(){
    const sendConfig = {
        type:"config",
        data:{
        mapEngine:config.value.mapEngine,
        mapOptions:{
            key:config.value.mapOptions.key
        }
    }
    }
    console.log(sendConfig)+
    websocketClient.value.ins.send(JSON.stringify(sendConfig))
    websocketClient.value.ins.onmessage = function(event){
        if(event.data == "done"){
            ElMessage(
                {
                    message:"配置提交成功，将在3秒后跳转至配置面板",
                    type:"success"
                }
            )
            setTimeout(()=>{
                router.push('/dashboard')
            },3000)
        }
    }
}
</script>

<template>
    <div id="configBeginning">
        <div id="notFinishText" v-if="!isFinishConfig" style="width:30rem ;">
            <el-row>
                <el-icon class="toBeCenter" size="120" color="#409EFC">
                    <Warning />
                </el-icon>
            </el-row>
            <el-row>
                <h1 id="header" class="toBeCenter">尚有配置未完成</h1>
            </el-row>
            <el-row>
                <h3 id="subheader" class="toBeCenter">Attention</h3>
            </el-row>

            <el-row>
                <h4 id="subheader" style="width:100%;margin-bottom: 0;">未完成的配置为：</h4>
            </el-row>
            <el-row>
                <ul class="description">
                    <li v-if="config.mapEngine == null">地图框架选择</li>
                    <li v-if="config.mapOptions.key == null">腾讯地图开发Key填 写</li>
                    <li v-if="config.options.domain == null">服务器域名填写</li>
                    <li v-if="config.options.port == null">服务器端口填写</li>
                    <li v-if="config.options.protocol == null">服务访问协议选择</li>
                    <li v-if="config.options.database == null">数据库类型选择</li>
                </ul>
            </el-row>
            <el-row>
                <h4 id="subheader" style="width:100%;">请点击下方按钮返回填写。</h4>
            </el-row> 
        </div>

        <div id="FinishText" v-else>
            <el-row>
                <el-icon class="toBeCenter" size="160" color="#409EFC"><Select /></el-icon>
            </el-row>

            <el-row>
                <h1 id="header" class="toBeCenter">配置已完成</h1>
            </el-row>
            <el-row>
                <h3 id="subheader" class="toBeCenter">WaitCommitting</h3>
            </el-row>
            <br>
            <el-row>
                <h4 id="subheader" style="width:100%;margin-bottom: 0;">您的配置为：</h4>
            </el-row>
            <el-row>
                <ul class="description">
                    <li>地图框架选择: {{config.mapEngine}}</li>
                    <li>腾讯地图开发Key: {{config.mapOptions.key}}</li>
                    <li>服务发布域名: {{config.options.domain}}</li>
                    <li>服务发布端口: {{config.options.port}}</li>
                    <li>服务访问协议: {{config.options.protocol}}</li>
                    <li>数据库类型: {{config.options.database}}</li>
                </ul>
            </el-row>
            <el-row>
                <el-alert v-if="!isConnectionOpened" title="由于未能与配置服务器连接，您暂时无法提交配置。" type="warning" show-icon :closable="false" />
            </el-row>
        </div>

        <div id="actionButton">
            <template v-if="!isFinishConfig">
                <el-row>
                    <el-button type="danger" size="large" @click="useConfigStepPre" class="toBeCenter">
                        <el-icon>
                            <ArrowLeft></ArrowLeft>
                        </el-icon> 返回填写
                    </el-button>
                </el-row>
            </template>
            <template v-else>
            <el-row>
                <el-button type="success" :loading="!isConnectionOpened" :loading-icon="Refresh" size="large" class="toBeCenter"
                    @click="commitConfig"> 提交配置
                </el-button>
            </el-row>
            </template>
            <!-- <el-row>
                <el-button type="success" :loading="!isConnectionOpened" size="large" class="toBeCenter"
                    @click="useConfigStepNext"> 提交配置 <el-icon>
                        <ArrowRight></ArrowRight>
                    </el-icon>
                </el-button>
            </el-row> -->
        </div>
    </div>


</template>

<style scoped>
p {
    margin-block-start: 0;
    margin-block-end: 0;
    margin-inline-start: 0;
    margin-inline-end: 0;
    display: flex;
}

.toBeCenter {
    margin: 0 auto;
}

.description {
    font-size: 1rem;
    color: #476582;
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
    margin: 2rem 25% 0 25%
}
</style>