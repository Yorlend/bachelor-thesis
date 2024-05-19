import { defineStore } from 'pinia'

export const useFpStore = defineStore({
  id: 'FpStore',
  state: () => ({
    fingerprints: [
      {
        "name": "fp_0",
        "position": {
          "x": 6.0,
          "y": 2.0
        }
      },
      {
        "name": "fp_1",
        "position": {
          "x": 2.0,
          "y": 2.0
        }
      },
      {
        "name": "fp_2",
        "position": {
          "x": 2.0,
          "y": 6.0
        }
      },
      {
        "name": "fp_3",
        "position": {
          "x": 5.0,
          "y": 6.0
        }
      },
      {
        "name": "fp_4",
        "position": {
          "x": 5.0,
          "y": 9.0
        }
      },
      {
        "name": "fp_5",
        "position": {
          "x": 1.0,
          "y": 9.0
        }
      },
      {
        "name": "fp_6",
        "position": {
          "x": 5.0,
          "y": 12.0
        }
      },
      {
        "name": "fp_7",
        "position": {
          "x": 3.0,
          "y": 15.0
        }
      },
      {
        "name": "fp_8",
        "position": {
          "x": 6.0,
          "y": 16.0
        }
      },
      {
        "name": "fp_9",
        "position": {
          "x": 4.0,
          "y": 17.0
        }
      },
      {
        "name": "fp_10",
        "position": {
          "x": 4.0,
          "y": 20.0
        }
      },
      {
        "name": "fp_11",
        "position": {
          "x": 6.0,
          "y": 20.0
        }
      },
      {
        "name": "fp_12",
        "position": {
          "x": 0.0,
          "y": 20.0
        }
      },
      {
        "name": "fp_13",
        "position": {
          "x": 1.0,
          "y": 23.0
        }
      },
      {
        "name": "fp_14",
        "position": {
          "x": 4.0,
          "y": 23.0
        }
      },
      {
        "name": "fp_15",
        "position": {
          "x": 6.0,
          "y": 23.0
        }
      },
      {
        "name": "fp_16",
        "position": {
          "x": 6.0,
          "y": 25.0
        }
      },
      {
        "name": "fp_17",
        "position": {
          "x": 3.0,
          "y": 25.0
        }
      },
      {
        "name": "fp_18",
        "position": {
          "x": 1.0,
          "y": 26.0
        }
      },
      {
        "name": "fp_19",
        "position": {
          "x": 1.0,
          "y": 28.0
        }
      },
      {
        "name": "fp_20",
        "position": {
          "x": 3.0,
          "y": 28.0
        }
      },
      {
        "name": "fp_21",
        "position": {
          "x": 5.0,
          "y": 30.0
        }
      },
      {
        "name": "fp_22",
        "position": {
          "x": 3.0,
          "y": 30.0
        }
      },
      {
        "name": "fp_23",
        "position": {
          "x": 0.0,
          "y": 30.0
        }
      }
    ]
  }),
  actions: {
    addFp(name: string, x: number, y: number) {
      this.fingerprints.push({name, position: { x, y } })
    },
    updatePos(name: string, x: number, y: number) {
      for (let fp of this.fingerprints) {
        if (fp.name === name) {
          fp.position = { x, y }
          break
        }
      }
    }
  },
})
