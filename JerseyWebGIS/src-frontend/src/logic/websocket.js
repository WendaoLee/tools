import {ref,watch} from 'vue'

const WEBSOCKEY_SERVER = "localhost"
const WEBSOCKEY_PORT = "1211"
// const WEBSOCKEY_SERVER = "localhost"

export let websocketClient = ref({
    ins:new WebSocket(`ws://${WEBSOCKEY_SERVER}:${WEBSOCKEY_PORT}/config`),
    count:0
})

let isConnectionOpened = ref(false)

function opended(){
    isConnectionOpened.value = true
}

websocketClient.value.ins.onclose = function reconnect(){
    setTimeout(()=>{
        isConnectionOpened.value = false
        websocketClient.value.ins = new WebSocket(`ws://${WEBSOCKEY_SERVER}:${WEBSOCKEY_PORT}/config`)
        websocketClient.value.ins.onclose = reconnect
        websocketClient.value.ins.onopen = opended
        websocketClient.value.count++
        console.log(websocketClient.value)
    },2000)
}

websocketClient.value.ins.onopen = opended


export function theWatcher(ref){
    return watch(ref,function(newVal,oldVal){
        console.log("yep")
        isConnectionOpened.value = newVal.ins.readyState == newVal.ins.OPEN
    })
}


export function useWebSocket(){
    return {isConnectionOpened,websocketClient}
}