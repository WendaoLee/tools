import {ref,computed} from 'vue'

const config = ref({
    step:0,
    mapEngine:null,
    mapOptions:{
        key:null
    },
    options:{
        protocol:null,
        domain:null,
        port:null,
        database:null,
        dbpath:null,
        dbaccount:null,
        dbpassword:null
    }
})

export const mapOptions =  [
    { label: '腾讯地图', value: 'TencentMap' }
]

export const protocolOptions = [
	{ label: 'http', value: 'http' },
	{ label: 'https', value: 'https' }
]

export const dbOptions = [
	{ label: 'sqlite', value: 'sqlite' }
]

export function useConfig(){
    return config
}

export function useConfigStepTo(num){
    config.value.step = num
}

export function useConfigStepNext(){
    config.value.step++
}

export function useConfigStepPre(){
    config.value.step--
}

export function useConfigWithIsFinishConfig(){
    const isFinishConfig = computed(()=>{
        let isFinishConfig = (config.value.mapEngine != null && config.value.mapOptions.key != null && config.value.options.protocol != null &&
            config.value.options.domain != null && config.value.options.port != null && config.value.options.database != null)
        return isFinishConfig
    })

    return {config,isFinishConfig}
}

