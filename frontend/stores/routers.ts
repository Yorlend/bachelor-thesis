import { defineStore } from 'pinia'
import { addRouter, deleteRouter, getRouters, updateRouter, type Router } from '@/lib/routers'

export const useRoutersStore = defineStore({
  id: 'routersStore',
  state: () => ({
    routers: [] as Router[]
  }),
  actions: {
    async get(): Promise<Router[]> {
      this.routers = await getRouters()
      return this.routers
    },
    async add(name: string, x: number, y: number) {
      await addRouter(name, x, y)
      this.routers.push({name, position: { x, y } })
    },
    async update(name: string, x: number, y: number) {
      await updateRouter(name, x, y)
      this.routers = this.routers.map((router) => {
        if (router.name === name) {
          router.position = { x, y }
        }
        return router
      })
    },
    async delete(name: string) {
      await deleteRouter(name)
      this.routers = this.routers.filter((router) => router.name !== name)
    }
  },
})
