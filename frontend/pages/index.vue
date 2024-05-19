<template>
  <div class="container flex flex-col justify-center items-center h-screen">
    <div class="flex flex-row">
      <TopoView class="border w-[800px] h-[350px] mr-5" :grid-enabled="false"></TopoView>
      <STabs default-value="fp" class="w-[500px]">
        <STabsList class="grid w-full grid-cols-2">
          <STabsTrigger value="fp">Опорные точки</STabsTrigger>
          <STabsTrigger value="routers">Точки доступа</STabsTrigger>
        </STabsList>
        <STabsContent value="fp">
          <SCard>
            <SCardHeader>
              <SCardTitle>Опорные точки</SCardTitle>
            </SCardHeader>
            <SCardContent class="space-y-2">
              <SScrollArea class="h-[400px]">
                <STable>
                  <STableCaption>Таблица опорных точек</STableCaption>
                  <STableHeader>
                    <STableHead>Имя</STableHead>
                    <STableHead>Координата X</STableHead>
                    <STableHead>Координата Y</STableHead>
                  </STableHeader>
                  <STableBody>
                    <STableRow v-for="fp in fpStore.fingerprints" :key="fp.name">
                      <STableCell>{{ fp.name }}</STableCell>
                      <STableCell>{{ fp.position.x }}</STableCell>
                      <STableCell>{{ fp.position.y }}</STableCell>
                      <STableCell>
                        <SButton variant="secondary" @click="onDeleteFp(fp.name)">
                          Удалить
                        </SButton>
                      </STableCell>
                    </STableRow>
                  </STableBody>
                </STable>
              </SScrollArea>
              <div class="flex justify-center">
                <SDialog>
                  <SDialogTrigger>
                    <SButton class="mt-5">Добавить</SButton>
                  </SDialogTrigger>
                  <SDialogContent>
                    <SDialogHeader>
                      <SDialogTitle>Добавление опорной точки</SDialogTitle>
                      <SDialogDescription>Введите название опорной точки и координаты</SDialogDescription>
                    </SDialogHeader>
                    <div class="grid gap-4 py-4">
                      <div class="grid grid-cols-3 items-center gap-4">
                        <SLabel for="name">Имя</SLabel>
                        <SInput id="name" class="col-span-3" v-model="newFpName" />
                      </div>
                      <div class="grid grid-cols-3 items-center gap-4">
                        <SLabel for="x">Координата X</SLabel>
                        <SInput id="x" class="col-span-3" v-model="newFpX" />
                      </div>
                      <div class="grid grid-cols-3 items-center gap-4">
                        <SLabel for="y">Координата Y</SLabel>
                        <SInput id="y" class="col-span-3" v-model="newFpY" />
                      </div>
                    </div>
                    <SDialogFooter>
                      <SButton type="submit" @click="onAddFp">
                        Добавить
                      </SButton>
                    </SDialogFooter>
                  </SDialogContent>
                </SDialog>
              </div>
            </SCardContent>
          </SCard>
        </STabsContent>
        <STabsContent value="routers">
          <SCard>
            <SCardHeader>
              <SCardTitle>Точки доступа</SCardTitle>
            </SCardHeader>
            <SCardContent class="space-y-2">
              <SScrollArea class="h-[400px]">
                <STable>
                  <STableCaption>Таблица точек доступа</STableCaption>
                  <STableHeader>
                    <STableHead>Имя</STableHead>
                    <STableHead>Координата X</STableHead>
                    <STableHead>Координата Y</STableHead>
                  </STableHeader>
                  <STableBody>
                    <STableRow v-for="r in routerStore.routers" :key="r.name">
                      <STableCell>{{ r.name }}</STableCell>
                      <STableCell>{{ r.position.x }}</STableCell>
                      <STableCell>{{ r.position.y }}</STableCell>
                      <STableCell>
                        <SButton variant="secondary" @click="onDeleteRouter(r.name)">
                          Удалить
                        </SButton>
                      </STableCell>
                    </STableRow>
                  </STableBody>
                </STable>
              </SScrollArea>
              <div class="flex justify-center">
                <SDialog>
                  <SDialogTrigger>
                    <SButton class="mt-5">Добавить</SButton>
                  </SDialogTrigger>
                  <SDialogContent>
                    <SDialogHeader>
                      <SDialogTitle>Добавление точки доступа</SDialogTitle>
                      <SDialogDescription>Введите название точки доступа и координаты</SDialogDescription>
                    </SDialogHeader>
                    <div class="grid gap-4 py-4">
                      <div class="grid grid-cols-3 items-center gap-4">
                        <SLabel for="name">Имя</SLabel>
                        <SInput id="name" class="col-span-3" v-model="newRouterName" />
                      </div>
                      <div class="grid grid-cols-3 items-center gap-4">
                        <SLabel for="x">Координата X</SLabel>
                        <SInput id="x" class="col-span-3" v-model="newRouterX" />
                      </div>
                      <div class="grid grid-cols-3 items-center gap-4">
                        <SLabel for="y">Координата Y</SLabel>
                        <SInput id="y" class="col-span-3" v-model="newRouterY" />
                      </div>
                    </div>
                    <SDialogFooter>
                      <SButton type="submit" @click="onAddRouter">
                        Добавить
                      </SButton>
                    </SDialogFooter>
                  </SDialogContent>
                </SDialog>
              </div>
            </SCardContent>
          </SCard>
        </STabsContent>
      </STabs>
    </div>

    <div class="flex flex-row">

    </div>
  </div>
</template>

<script lang="ts" setup>
const fpStore = useFpStore()
const routerStore = useRoutersStore()

const newFpName = ref("")
const newRouterName = ref("")

const newFpX = ref("")
const newFpY = ref("")

const newRouterX = ref("")
const newRouterY = ref("")

const onAddFp = () => {
  if (newFpName.value.trim() === "") return
  if (isNaN(+newFpX.value) || isNaN(+newFpY.value)) return
  fpStore.fingerprints.push({ name: newFpName.value, position: { x: +newFpX.value, y: +newFpY.value } })

  newFpName.value = ""
  newFpX.value = ""
  newFpY.value = ""
}

const onAddRouter = () => {
  if (newRouterName.value.trim() === "") return
  if (isNaN(+newRouterX.value) || isNaN(+newRouterY.value)) return
  routerStore.routers.push({ name: newRouterName.value, position: { x: +newRouterX.value, y: +newRouterY.value } })

  newRouterName.value = ""
  newRouterX.value = ""
  newRouterY.value = ""
}

const onDeleteFp = (fpName: string) => {
  fpStore.fingerprints = fpStore.fingerprints.filter((fp) => fp.name !== fpName)
}

const onDeleteRouter = (routerName: string) => {
  routerStore.routers = routerStore.routers.filter((router) => router.name !== routerName)
}

</script>

<style scoped></style>