<script setup>
import { Menu as IconMenu } from '@element-plus/icons-vue'
import { ResetCategory } from '@/logic/dashboardapi'
import DashboardCategoryTableVue from '@/components/DashboardCategoryTable.vue'
import TencentMapAddVue from '@/components/TencentMapAdd.vue';
import TencentMapInfoVue from '@/components/TencentMapInfo.vue'
import { useDashboardStep, changeTargetStep } from '@/logic/dashboardstep'

const targetStep = useDashboardStep()

ResetCategory()
</script>

<template>
  <div class="common-layout">
    <el-container class="layout-container-demo" style="height: 500px">
      <el-header>JerseyWebGIS</el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu default-active="1">
            <el-menu-item index="1" @click="changeTargetStep('infotable')">
              <el-icon>
                <IconMenu />
              </el-icon>
              类型面板
            </el-menu-item>
            <el-menu-item index="2" @click="changeTargetStep('pointadd')">
              <el-icon>
                <IconMenu />
              </el-icon>
              添加采集点
            </el-menu-item>
            <el-menu-item index="3" @click="changeTargetStep('service')">
              <el-icon>
                <IconMenu />
              </el-icon>
              服务层查看
            </el-menu-item>
            <!-- <el-sub-menu index="1">
                <template>
                  <el-icon><IconMenu/></el-icon>
                  <span>欢迎</span>
                </template>
              </el-sub-menu> -->
          </el-menu>
        </el-aside>
        <el-main>
        
          <Transition name="fade" mode="out-in">
            <template v-if="targetStep == 'infotable'">
              <DashboardCategoryTableVue></DashboardCategoryTableVue>
            </template>
            <template v-else-if="targetStep == 'pointadd'" :key="targetStep">
                  <TencentMapAddVue></TencentMapAddVue>
            </template>
            <template v-else>
              <TencentMapInfoVue></TencentMapInfoVue>
            </template>
          </Transition>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
  
<style scoped>
.layout-container-demo .el-header {
  position: relative;
  background-color: rgb(48, 65, 86);
  color: var(--el-text-color-primary);
}

.layout-container-demo .el-aside {
  color: var(--el-text-color-primary);
  background: rgb(48, 65, 86);
  height: 60rem;
}

.layout-container-demo .el-menu {
  border-right: none;
  background: rgb(48, 65, 86);
}

.layout-container-demo .el-main {
  padding: 0;
  width: 100%;
  height: 100%;
}

.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 80rem;
  right: 20px;
}

.el-menu-item{
  color:white
}

</style>
