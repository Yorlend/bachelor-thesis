import { defineStore } from 'pinia'
import { createFP, deleteFP, getFPs, updateFP, type Fingerprint } from '~/lib/fp'

export const useFpStore = defineStore({
  id: 'FpStore',
  state: () => ({
    fingerprints: [] as Fingerprint[]
  }),
  actions: {
    async get(): Promise<Fingerprint[]> {
      this.fingerprints = await getFPs()
      return this.fingerprints
    },
    async add(name: string, x: number, y: number) {
      await createFP(name, x, y)
      this.fingerprints.push({ name, position: { x, y } })
    },
    async update(name: string, x: number, y: number) {
      await updateFP(name, x, y)
      this.fingerprints = this.fingerprints.map((fp) => {
          if (fp.name === name) {
            fp.position = { x, y }
          }
          return fp
        }
      )
    },
    async delete(name: string) {
      await deleteFP(name)
      this.fingerprints = this.fingerprints.filter((fp) => fp.name !== name)
    }
  },
})
