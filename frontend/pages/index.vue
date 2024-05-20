<template>
  <div class="container flex flex-col justify-center items-stretch h-screen">
    <TopoView class="border h-[800px] mr-5" :grid-enabled="false"></TopoView>

    <SButton class="my-5" @click="$router.push('/config')">К конфигурации</SButton>

    <div class="flex flex-row justify-between items-center"></div>
    <div class="flex flex-col">
      <span class="my-5">Информация об агенте</span>
      <div class="grid grid-cols-2 items-center gap-6">
        <SLabel for="x">Координата X</SLabel>
        <SInput id="x" class="col-span-1" v-model="agentStore.position.x" />
        <SLabel for="y">Координата Y</SLabel>
        <SInput id="y" class="col-span-1" v-model="agentStore.position.y" />
      </div>
    </div>
    <div class="flex flex-col justify-end my-5">
      <SButton class="my-5" @click="onLocalize">Геопозиционировать</SButton>
      <div class="grid grid-cols-2 gap-6">
        <span>Позиция: </span>
        <span>{{ Math.round(agentStore.predicted.x * 100) / 100 }}, {{ Math.round(agentStore.predicted.y * 100) / 100
          }}</span>
        <span>Расстояние до ближайшей опорной точки: </span>
        <span>{{ Math.round(agentStore.proximity * 100) / 100 }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { localize } from '~/lib/positioning';


const agentStore = useAgentStore()

const onLocalize = async () => {
  const res = await localize(agentStore.position.x, agentStore.position.y)

  if (res) {
    agentStore.predicted.x = res.x
    agentStore.predicted.y = res.y
    agentStore.proximity = res.distance
  }
}

</script>

<style scoped></style>