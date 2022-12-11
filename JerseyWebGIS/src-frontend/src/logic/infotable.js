import { ref } from "vue";

isShow = ref(false)

export function useIsShow(){
    return isShow
}