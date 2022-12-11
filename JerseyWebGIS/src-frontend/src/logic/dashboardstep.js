import {ref} from 'vue'

const targetStep = ref('infotable')

export function useDashboardStep(){
    return targetStep
}

export function changeTargetStep(newStep){
    targetStep.value = newStep
}