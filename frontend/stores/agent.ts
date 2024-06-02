import { defineStore } from "pinia";

export const useAgentStore = defineStore({
  id: "agentStore",
  state: () => ({
    position: { x: NaN, y: NaN },
    predicted: { x: NaN, y: NaN },
    closest: { x: NaN, y: NaN },
  }),
  actions: {
    updatePosition(x: number, y: number) {
      this.position.x = x;
      this.position.y = y;
    },
    updatePredicted(x: number, y: number) {
      this.predicted.x = x;
      this.predicted.y = y;
    },
  },
});
