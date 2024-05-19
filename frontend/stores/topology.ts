import { defineStore } from 'pinia'

export const useTopologyStore = defineStore({
  id: 'topologyStore',
  state: () => ({
    vertices: [
        { x: 0, y: 0 },
        { x: 0, y: 50 },
        { x: 50, y: 50 },
        { x: 50, y: 0 },
    ],
   }),
  actions: {
    moveVertexTo(index: number, newX: number, newY: number) {
        this.vertices[index] = { x: newX, y: newY }
    },
    insertVertexAfter(index: number) {
        const x1 = this.vertices[index].x
        const y1 = this.vertices[index].y
        const x2 = this.vertices[(index + 1) % this.vertices.length].x
        const y2 = this.vertices[(index + 1) % this.vertices.length].y
        const x = (x1 + x2) / 2
        const y = (y1 + y2) / 2
        this.vertices.splice(index+1, 0, {x, y})
    },
    removeVertex(index: number) {
        this.vertices.splice(index, 1)
    }
  }
})
