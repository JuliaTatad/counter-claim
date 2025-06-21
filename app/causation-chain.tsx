"use client"

import {
  type Node,
  type Edge,
  Background,
  Controls,
  MiniMap,
  ReactFlowProvider,
  Handle,
  Position,
  useNodesState,
  useEdgesState,
  ReactFlow,
  MarkerType,
  BackgroundVariant,
} from "reactflow"
import "reactflow/dist/style.css"

// Custom node component for different node types
const CustomNode = ({ data }: { data: any }) => {
  const getNodeStyle = (group: string) => {
    switch (group) {
      case "event":
        return {
          background: "#e3f2fd",
          border: "2px solid #1976d2",
          borderRadius: "8px",
          color: "#1976d2",
        }
      case "claim":
        return {
          background: "#fff3e0",
          border: "2px solid #f57c00",
          borderRadius: "8px",
          color: "#f57c00",
        }
      case "evidence":
        return {
          background: "#ffebee",
          border: "2px solid #d32f2f",
          borderRadius: "4px",
          color: "#d32f2f",
        }
      case "legal_standard":
        return {
          background: "#f3e5f5",
          border: "2px solid #7b1fa2",
          borderRadius: "4px",
          color: "#7b1fa2",
        }
      case "weakness":
        return {
          background: "#ffcdd2",
          border: "2px dashed #f44336",
          borderRadius: "4px",
          color: "#c62828",
        }
      default:
        return {
          background: "#f5f5f5",
          border: "2px solid #666",
          borderRadius: "8px",
          color: "#333",
        }
    }
  }

  const style = getNodeStyle(data.group)

  return (
    <div
      style={{
        ...style,
        padding: "12px 16px",
        minWidth: "180px",
        textAlign: "center",
        fontSize: "14px",
        fontWeight: "500",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
      }}
    >
      <Handle type="target" position={Position.Top} />
      <div>{data.label}</div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}

const nodeTypes = {
  custom: CustomNode,
}

// Based on the report's analysis of Kronos's counterclaim
const initialNodes: Node[] = [
  {
    id: "mining",
    type: "custom",
    position: { x: 400, y: 50 },
    data: { label: "Fenoscadia Mining Operations (80-year concession)", group: "event" },
    draggable: true,
  },
  {
    id: "contamination",
    type: "custom",
    position: { x: 400, y: 180 },
    data: { label: "Alleged Rhea River Contamination", group: "event" },
    draggable: true,
  },
  {
    id: "health",
    type: "custom",
    position: { x: 400, y: 310 },
    data: { label: "Public Health Impact Claims", group: "event" },
    draggable: true,
  },
  {
    id: "damages",
    type: "custom",
    position: { x: 400, y: 440 },
    data: { label: "USD 150M Damages Claim", group: "claim" },
    draggable: true,
  },
  {
    id: "study",
    type: "custom",
    position: { x: 100, y: 250 },
    data: { label: "University Study (INCONCLUSIVE)", group: "weakness" },
    draggable: true,
  },
  {
    id: "burlington",
    type: "custom",
    position: { x: 700, y: 180 },
    data: { label: "Burlington Standard: 'Clear & Convincing Evidence'", group: "legal_standard" },
    draggable: true,
  },
  {
    id: "causation_gap",
    type: "custom",
    position: { x: 100, y: 380 },
    data: { label: "80-Year Timeline Complicates Causation", group: "weakness" },
    draggable: true,
  },
  {
    id: "quantum_gap",
    type: "custom",
    position: { x: 700, y: 380 },
    data: { label: "No Transparent Damage Methodology", group: "weakness" },
    draggable: true,
  },
]

const initialEdges: Edge[] = [
  {
    id: "mining-contamination",
    source: "mining",
    target: "contamination",
    label: "allegedly causes",
    style: { stroke: "#666", strokeWidth: 2 },
    markerEnd: { type: MarkerType.ArrowClosed, color: "#666" },
  },
  {
    id: "contamination-health",
    source: "contamination",
    target: "health",
    label: "allegedly causes",
    style: { stroke: "#666", strokeWidth: 2 },
    markerEnd: { type: MarkerType.ArrowClosed, color: "#666" },
  },
  {
    id: "health-damages",
    source: "health",
    target: "damages",
    label: "justifies",
    style: { stroke: "#666", strokeWidth: 2 },
    markerEnd: { type: MarkerType.ArrowClosed, color: "#666" },
  },
  {
    id: "study-contamination",
    source: "study",
    target: "contamination",
    label: "weak evidence",
    style: { stroke: "#f44336", strokeWidth: 2, strokeDasharray: "5,5" },
    markerEnd: { type: MarkerType.ArrowClosed, color: "#f44336" },
  },
  {
    id: "burlington-contamination",
    source: "burlington",
    target: "contamination",
    label: "challenges proof standard",
    style: { stroke: "#7b1fa2", strokeWidth: 2, strokeDasharray: "5,5" },
    markerEnd: { type: MarkerType.ArrowClosed, color: "#7b1fa2" },
  },
  {
    id: "causation_gap-health",
    source: "causation_gap",
    target: "health",
    label: "undermines link",
    style: { stroke: "#f44336", strokeWidth: 2, strokeDasharray: "5,5" },
    markerEnd: { type: MarkerType.ArrowClosed, color: "#f44336" },
  },
  {
    id: "quantum_gap-damages",
    source: "quantum_gap",
    target: "damages",
    label: "undermines calculation",
    style: { stroke: "#f44336", strokeWidth: 2, strokeDasharray: "5,5" },
    markerEnd: { type: MarkerType.ArrowClosed, color: "#f44336" },
  },
]

export default function CausationChain() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)

  return (
    <div className="w-full h-screen bg-white">
      <div className="p-4 bg-gray-50 border-b">
        <h1 className="text-2xl font-bold text-gray-900">Kronos Environmental Counterclaim - Causation Analysis</h1>
        <p className="text-gray-600 mt-1">
          Fenoscadia v. Kronos - Identifying vulnerabilities in the USD 150M counterclaim
        </p>
        <p className="text-sm text-blue-600 mt-1">💡 Red dashed lines show your strongest attack points</p>
        <div className="flex gap-6 mt-3 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-100 border-2 border-blue-600 rounded"></div>
            <span>Events</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-orange-100 border-2 border-orange-600 rounded"></div>
            <span>Claims</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-red-100 border-2 border-red-600 rounded"></div>
            <span>Critical Weaknesses</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-purple-100 border-2 border-purple-600 rounded"></div>
            <span>Legal Standards</span>
          </div>
        </div>
      </div>
      <div style={{ width: '100%', height: '100vh' }}>
        <ReactFlowProvider>
          <ReactFlow
            nodes={nodes}
            edges={edges}
          nodeTypes={nodeTypes}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
          attributionPosition="bottom-left"
        >
          <Background variant={BackgroundVariant.Dots} gap={20} size={1} />
          <Controls />
          <MiniMap
            nodeColor={(node) => {
              switch (node.data.group) {
                case "event":
                  return "#1976d2"
                case "claim":
                  return "#f57c00"
                case "weakness":
                  return "#f44336"
                case "legal_standard":
                  return "#7b1fa2"
                default:
                  return "#666"
              }
            }}
            />
          </ReactFlow>
        </ReactFlowProvider>
      </div>
    </div>
  )
}
