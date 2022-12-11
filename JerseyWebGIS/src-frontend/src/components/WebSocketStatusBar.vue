<script setup>
import {useWebSocket} from '@/logic/websocket.js'
import {watch} from 'vue'

const {isConnectionOpened,websocketClient} = useWebSocket()

</script>

<template>
    <div id="WebsocketStatus" v-if="!isConnectionOpened">
        <el-alert title="与配置服务器的连接丢失，正在尝试重连中。您仍然可以继续配置，不过您无法在重连前提交配置。" center type="error" effect="dark" :closable="false" show-icon />
    </div>
</template>