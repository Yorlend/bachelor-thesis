import { defineStore } from 'pinia'

export const useRoutersStore = defineStore({
  id: 'routersStore',
  state: () => ({
    routers: [
      {
        name: 'router_0',
        position: {
          x: 10.0,
          y: 40.0,
        }
      },
      {
        name: 'router_1',
        position: {
          x: 2.0,
          y: 2.0,
        }
      },
      {
        name: 'router_2',
        position: {
          x: 9.0,
          y: 4.0,
        }
      }
    ]
  }),
  actions: {
    addRouter(name: string, x: number, y: number) {
      this.routers.push({name, position: { x, y } })
    },
    updatePos(name: string, x: number, y: number) {
      for (let router of this.routers) {
        if (router.name === name) {
          router.position = { x, y }
          break
        }
      }
    }
  },
})
