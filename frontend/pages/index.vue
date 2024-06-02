<template>
  <div class="container flex flex-col justify-center items-stretch gap-2 h-screen">
    <TopoView class="border h-[800px]" :grid-enabled="false"></TopoView>

    <div class="grid grid-cols-2 gap-2">
      <SButton @click="$router.push('/config')">К конфигурации</SButton>
      <OptimizerPopup />
    </div>
    <SButton @click="onLocalize">Геопозиционировать</SButton>

    <span class="mt-2">Информация об агенте</span>
    <div class="flex flex-col">
      <div class="grid grid-cols-2 gap-6">
        <div class="grid grid-cols-3 gap-6">
          <SLabel for="x">Координата X</SLabel>
          <SInput id="x" class="col-span-2" v-model="agentStore.position.x" />
          <SLabel for="y">Координата Y</SLabel>
          <SInput id="y" class="col-span-2" v-model="agentStore.position.y" />
        </div>
        <div class="grid grid-cols-2 gap-6">
          <span>Предсказанная позиция:</span>
          <span>{{ Math.round(agentStore.predicted.x * 100) / 100 }}, {{ Math.round(agentStore.predicted.y * 100) / 100
            }}</span>
          <span>Координаты ближайшей опорной точки: </span>
          <span>{{ Math.round(agentStore.closest.x * 100) / 100 }}, {{ Math.round(agentStore.closest.y * 100) / 100
            }}</span>
        </div>
      </div>
    </div>
    <div class="flex flex-col justify-end my-5">
    </div>
  </div>
</template>

<script lang="ts" setup>
import OptimizerPopup from '~/components/OptimizerPopup.vue';
import { localize } from '~/lib/positioning';


const agentStore = useAgentStore()

const onLocalize = async () => {
  const res = await localize(agentStore.position.x, agentStore.position.y)

  if (res) {
    agentStore.predicted.x = res.x
    agentStore.predicted.y = res.y
    agentStore.closest.x = res.closest_x
    agentStore.closest.y = res.closest_y
  }
}

</script>

<style scoped></style>