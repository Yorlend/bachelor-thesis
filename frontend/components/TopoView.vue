<script setup lang="ts">
import { VNetworkGraph, defineConfigs, GridLayout, type ViewConfig, SimpleLayout, type Instance, type EventHandlers } from 'v-network-graph'
import type { RecursivePartial } from 'v-network-graph/lib/common/common.js'
import { useFpStore } from '@/stores/fp'
import { useRoutersStore } from '~/stores/routers'

const fpStore = useFpStore()
const routerStore = useRoutersStore()

const props = defineProps({
  gridEnabled: { type: Boolean, default: false }
})

// ref="graph"
const graph = ref<Instance>()

const nodes: any = reactive({
  // topology nodes
  node1: { color: 'black' },
  node2: { color: 'black' },
  node3: { color: 'black' },
  node4: { color: 'black' },
})

const edges = reactive({
  edge1: { source: "node1", target: "node2" },
  edge2: { source: "node2", target: "node3" },
  edge3: { source: "node3", target: "node4" },
  edge4: { source: "node4", target: "node1" },
})

const layouts: any = reactive({
  nodes: {
    node1: { x: 0, y: 0 },
    node2: { x: 50, y: 0 },
    node3: { x: 50, y: 50 },
    node4: { x: 0, y: 50 },
  }
})

function updateGeometry() {
  // clear all fp and router nodes
  for (let nodeName in nodes) {
    if (nodes[nodeName].isFp || nodes[nodeName].isRouter) {
      delete nodes[nodeName]
    }
  }

  for (let fpIndex in fpStore.fingerprints) {
    const fp = fpStore.fingerprints[fpIndex]
    nodes[`fp${fpIndex}`] = {
      color: 'green',
      name: fp.name,
      isFp: true,
    }
    layouts.nodes[`fp${fpIndex}`] = {
      x: fp.position.x,
      y: fp.position.y,

    }
  }

  for (let routerIndex in routerStore.routers) {
    const router = routerStore.routers[routerIndex]
    nodes[`router${routerIndex}`] = {
      color: 'red',
      name: router.name,
      isRouter: true,
    }
    layouts.nodes[`router${routerIndex}`] = {
      x: router.position.x,
      y: router.position.y,
    }
  }
}

fpStore.$subscribe(updateGeometry)
routerStore.$subscribe(updateGeometry)

onMounted(() => {
  updateGeometry()
})

const viewConfig: RecursivePartial<ViewConfig> = reactive(
  {
    minZoomLevel: 4,
    maxZoomLevel: 10,
    autoPanAndZoomOnLoad: "center-content",

    panEnabled: true,
    zoomEnabled: true,
    grid: {
      visible: true,
      interval: 5,
      thickIncrements: 5,
      line: {
        color: "#e0e0e0",
        width: 1,
        dasharray: 1,
      },
      thick: {
        color: "#cccccc",
        width: 1,
        dasharray: 0,
      },
    },
  }
)

watchEffect(() => {
  viewConfig.layoutHandler = props.gridEnabled ? new GridLayout({ grid: 5 }) : new SimpleLayout()
})

const configs = reactive(
  defineConfigs({
    node: {
      label: {
        visible: true,
        direction: "south",
        directionAutoAdjustment: true,
      },
      normal: {
        type: 'circle',
        radius: 5,
        color: node => node.color,
      }
    },
    edge: {
      normal: {
        color: 'black',
      },
    },
    view: viewConfig,
  })
)


// ref="tooltip"
const tooltip = ref<HTMLDivElement>()

const targetNodeId = ref<string>("")
const tooltipOpacity = ref(0) // 0 or 1
const tooltipPos = ref({ left: "0px", top: "0px" })

const targetNodePos = computed(() => {
  const nodePos = layouts.nodes[targetNodeId.value]
  return nodePos || { x: 0, y: 0 }
})

// Update `tooltipPos`
watch(
  () => [targetNodePos.value, tooltipOpacity.value],
  () => {
    if (!graph.value || !tooltip.value) return

    // translate coordinates: SVG -> DOM
    const domPoint = graph.value.translateFromSvgToDomCoordinates(targetNodePos.value)
    // calculates top-left position of the tooltip.
    tooltipPos.value = {
      left: domPoint.x - tooltip.value.offsetWidth / 2 + "px",
      top: domPoint.y - 20 - tooltip.value.offsetHeight - 10 + "px",
    }
  },
  { deep: true }
)

const eventHandlers: EventHandlers = {
  "node:pointerover": ({ node }) => {
    if (nodes[node].isFp || nodes[node].isRouter) {
      targetNodeId.value = node
      tooltipOpacity.value = 1 // show
    }
  },
  "node:pointerout": _ => {
    tooltipOpacity.value = 0 // hide
  },
}

const zoomLevel = ref(4)
</script>

<template>
  <div class="tooltip-wrapper">
    <v-network-graph class="graph" ref="graph" :nodes="nodes" :edges="edges" :layouts="layouts" :zoom-level="zoomLevel"
      :configs="configs" :event-handlers="eventHandlers" />
    <!-- Tooltip -->
    <div ref="tooltip" class="tooltip" :style="{ ...tooltipPos, opacity: tooltipOpacity }">
      <div>{{ nodes[targetNodeId]?.name ?? "" }}</div>
    </div>
  </div>
</template>

<style scoped>
.graph {
  width: 800px;
  height: 600px;
}

.tooltip-wrapper {
  position: relative;
}

.tooltip {
  top: 0;
  left: 0;
  opacity: 0;
  position: absolute;
  width: 80px;
  height: 36px;
  display: grid;
  place-content: center;
  text-align: center;
  font-size: 12px;
  background-color: #fff0bd;
  border: 1px solid #ffb950;
  box-shadow: 2px 2px 2px #aaa;
  transition: opacity 0.2s linear;
  pointer-events: none;
}
</style>
