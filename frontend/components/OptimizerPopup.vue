<template>
  <SDialog>
    <SDialogTrigger>
      <SButton class="w-full">Оптимизировать положение опорных точек</SButton>
    </SDialogTrigger>
    <SDialogContent>
      <SDialogHeader>
        <SDialogTitle>Оптимизация положения опорных точек</SDialogTitle>
        <SDialogDescription>Введите параметры оптимизации методом роя частиц</SDialogDescription>
      </SDialogHeader>
      <div class="grid gap-4 py-4">
        <div class="grid grid-cols-3 items-center gap-4">
          <SLabel for="name">Количество частиц</SLabel>
          <SInput id="name" class="col-span-2" v-model="particlesCount" :disabled="isRunning" />
        </div>
        <div class="grid grid-cols-3 items-center gap-4">
          <SLabel for="name">Количество итераций</SLabel>
          <SInput id="name" class="col-span-2" v-model="iterationsCount" :disabled="isRunning" />
        </div>
      </div>
      <SProgress v-if="isRunning" :model-value="progress" />
      <SDialogFooter>
        <div class="flex flex-row items-baseline gap-4">
          <div class="text-green-800" v-if="isDone">
            Оптимизация завершена
          </div>
          <SButton type="submit" @click="startStopOptimization">
            {{ isRunning ? 'Остановить' : 'Запустить' }}
          </SButton>
        </div>
      </SDialogFooter>
    </SDialogContent>
  </SDialog>
</template>

<script lang="ts" setup>
import { cancelOptimization, getProgress, optimizationDone, startOptimization } from '~/lib/optimization';


const particlesCount = ref(100)
const iterationsCount = ref(10)

const isRunning = ref(false)
const isDone = ref(false)
const progress = ref(0)

const fpStore = useFpStore()

async function startStopOptimization() {
  isRunning.value = !isRunning.value
  if (isRunning.value) {
    isDone.value = false
    await startOptimization(iterationsCount.value, particlesCount.value)
  } else {
    await cancelOptimization()
  }
}

onMounted(async () => {
  setInterval(async () => {
    if (isRunning.value) {
      if (await optimizationDone()) {
        progress.value = 100
        isRunning.value = false
        isDone.value = true
        // update fp store
        await fpStore.get()
      } else {
        progress.value = await getProgress()
      }
    }
  }, 1000)
})

</script>
