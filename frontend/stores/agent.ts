import { defineStore } from 'pinia'

export const useAgentStore = defineStore({
  id: 'agentStore',
  state: () => ({
    x: 20.0,
    y: 10.0
  }),
})
