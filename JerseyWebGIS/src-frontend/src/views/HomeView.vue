<script setup>
import WebSocketStatusBarVue from '../components/WebSocketStatusBar.vue'
import ConfigStepFirstBeginVue from '@/components/ConfigStepFirst.begin.vue'
import ConfigStepSecondMapchooseVue from '@/components/ConfigStepSecond.mapchoose.vue'
import ConfigStepThirdServeroptionsVue from '@/components/ConfigStepThird.serveroptions.vue'
import ConfigStepForthFinalVue from '@/components/ConfigStepForth.final.vue'
import { useConfig } from '@/logic/setupconfig'

const config = useConfig()
</script>

<template>
    <WebSocketStatusBarVue></WebSocketStatusBarVue>
    <el-container>
        <el-header class="needTopOffset">
            <el-steps :active="config.step" finish-status="success" align-center>
                <el-step title="开始" description="于此开始您的配置"></el-step>
                <el-step title="选择地图框架" description="使用的地图渲染容器"></el-step>
                <el-step title="配置服务器参数" description="发布的服务的域名地址、数据库配置等参数"></el-step>
                <el-step title="完成" description="进入配置面板以获取更多"></el-step>
            </el-steps>
        </el-header>
        <el-main class="contentCenter needTopOffset">
            <Transition name="fade" mode="out-in">
                <template v-if="config.step == 0">
                    <ConfigStepFirstBeginVue></ConfigStepFirstBeginVue>
                </template>
                <template v-else-if="config.step == 1">
                    <ConfigStepSecondMapchooseVue></ConfigStepSecondMapchooseVue>
                </template>
                <template v-else-if="config.step == 2">
                    <ConfigStepThirdServeroptionsVue></ConfigStepThirdServeroptionsVue>
                </template>
                <template v-else-if="config.step == 3">
                <ConfigStepForthFinalVue></ConfigStepForthFinalVue>
                </template>
            </Transition>
        </el-main>
    </el-container>
</template>

<style scoped>
.needTopOffset {
    margin-top: 1rem;
}

.contentCenter {
    align-self: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

</style>
