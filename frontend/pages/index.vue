<template>
  <div class="container flex flex-col justify-center items-stretch h-screen">
    <TopoView class="border h-[800px] mr-5" :grid-enabled="false"></TopoView>

    <SButton class="my-5" @click="$router.push('/config')">К конфигурации</SButton>

    <div class="flex flex-row justify-between items-center"></div>
    <div class="flex flex-col">
      <span class="my-5">Информация об агенте</span>
      <div class="grid grid-cols-2 items-center gap-6">
        <SLabel for="x">Координата X</SLabel>
        <SInput id="x" class="col-span-1" v-model="agentX" />
        <SLabel for="y">Координата Y</SLabel>
        <SInput id="y" class="col-span-1" v-model="agentY" />
      </div>
    </div>
    <div class="flex flex-col justify-end my-5">
      <SButton class="my-5">Геопозиционировать</SButton>
      <div class="grid grid-cols-2 gap-6">
        <span>Позиция: </span>
        <span>NaN</span>
        <span>Расстояние до ближайшей опорной точки: </span>
        <span>NaN</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>

const agentX = ref("")
const agentY = ref("")

</script>

<style scoped></style>