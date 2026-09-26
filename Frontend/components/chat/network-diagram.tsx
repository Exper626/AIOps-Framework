"use client";

import "@xyflow/react/dist/style.css";
import {
  applyEdgeChanges,
  applyNodeChanges,
  Background,
  BaseEdge,
  type Connection,
  ConnectionMode,
  Controls,
  type Edge,
  type EdgeChange,
  type EdgeProps,
  getStraightPath,
  Handle,
  type InternalNode,
  type Node,
  type NodeChange,
  type NodeProps,
  Panel,
  Position,
  ReactFlow,
  ReactFlowProvider,
  useConnection,
  useInternalNode,
  useReactFlow,
} from "@xyflow/react";
import {
  DownloadIcon,
  LayoutGridIcon,
  PlusIcon,
  Trash2Icon,
} from "lucide-react";
import Image from "next/image";
import { useTheme } from "next-themes";
import {
  type CSSProperties,
  createContext,
  type FocusEvent,
  type KeyboardEvent,
  type MouseEvent,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { toast } from "sonner";
import {
  DEVICE_TYPES,
  iconFor,
  layoutDiagram,
  type NetworkDiagram,
  nextDeviceName,
} from "@/lib/diagram";
import { downloadDiagramImage } from "@/lib/diagram-image";
import { cn, generateUUID } from "@/lib/utils";
import { Button } from "../ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";
import { WithTooltip } from "./with-tooltip";

type DeviceData = { name: string; type: string; model: string };
type DeviceNode = Node<DeviceData, "device">;

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const DEVICE_WIDTH = 96;
const DEVICE_HEIGHT = 76;

type DiagramContextValue = {
  editingId: string | null;
  readOnly: boolean;
  stopEditing: () => void;
};

const DiagramContext = createContext<DiagramContextValue>({
  editingId: null,
  readOnly: false,
  stopEditing: () => null,
});

function toNodes(diagram: NetworkDiagram): DeviceNode[] {
  const positions = layoutDiagram(diagram);

  return diagram.devices.map((device) => ({
    data: { model: device.model ?? "", name: device.name, type: device.type },
    id: device.id,
    position: positions.get(device.id) ?? { x: 0, y: 0 },
    type: "device",
  }));
}

function toEdges(diagram: NetworkDiagram): Edge[] {
  return diagram.links.map((link) => ({
    id: `${link.source}->${link.target}`,
    source: link.source,
    target: link.target,
    type: "cable",
  }));
}

function toDiagram(nodes: DeviceNode[], edges: Edge[]): NetworkDiagram {
  return {
    devices: nodes.map((node) => ({
      id: node.id,
      model: node.data.model,
      name: node.data.name,
      type: node.data.type,
      x: Math.round(node.position.x),
      y: Math.round(node.position.y),
    })),
    links: edges.map((edge) => ({ source: edge.source, target: edge.target })),
  };
}

// One cable between two devices, whichever way it was drawn
function isNewCable(connection: Connection | Edge, edges: Edge[]) {
  const { source, target } = connection;

  return (
    source !== target &&
    !edges.some(
      (edge) =>
        (edge.source === source && edge.target === target) ||
        (edge.source === target && edge.target === source)
    )
  );
}

function freeSpot(point: { x: number; y: number }, nodes: DeviceNode[]) {
  const spot = { ...point };

  for (let tries = 0; tries < 20; tries += 1) {
    const taken = nodes.some(
      (node) =>
        Math.abs(node.position.x - spot.x) < DEVICE_WIDTH + 16 &&
        Math.abs(node.position.y - spot.y) < DEVICE_HEIGHT + 16
    );

    if (!taken) {
      break;
    }

    spot.x += DEVICE_WIDTH + 24;
  }

  return spot;
}

function DeviceIcon({ type, size }: { type: string; size: number }) {
  return (
    <Image
      alt=""
      className="pointer-events-none select-none object-contain"
      draggable={false}
      height={size}
      src={`${BASE_PATH}${iconFor(type)}`}
      style={{ height: size, width: size }}
      unoptimized
      width={size}
    />
  );
}

// The drop area covers the whole device while a cable is being drawn, so the
// cable can be let go anywhere on it
const DROP_AREA: CSSProperties = {
  background: "transparent",
  border: 0,
  borderRadius: 12,
  height: "100%",
  left: 0,
  top: 0,
  transform: "none",
  width: "100%",
};

// Enter or leaving the fields saves, Escape keeps the old name
function DeviceForm({ id, data }: { id: string; data: DeviceData }) {
  const { updateNodeData } = useReactFlow();
  const { stopEditing } = useContext(DiagramContext);

  const save = useCallback(
    (form: HTMLFormElement) => {
      const fields = new FormData(form);
      const name = String(fields.get("name") ?? "").trim();

      updateNodeData(id, {
        model: String(fields.get("model") ?? "").trim(),
        name: name || data.name,
      });
      stopEditing();
    },
    [data.name, id, stopEditing, updateNodeData]
  );

  const handleBlur = useCallback(
    (event: FocusEvent<HTMLInputElement>) => {
      const { form } = event.currentTarget;

      if (form && !form.contains(event.relatedTarget)) {
        save(form);
      }
    },
    [save]
  );

  const handleKeyDown = useCallback(
    (event: KeyboardEvent<HTMLInputElement>) => {
      const { form } = event.currentTarget;

      if (event.key === "Enter" && form) {
        event.preventDefault();
        save(form);
      } else if (event.key === "Escape") {
        stopEditing();
      }
    },
    [save, stopEditing]
  );

  return (
    <form className="nodrag flex w-full flex-col gap-1">
      <input
        aria-label="Device name"
        autoFocus
        className="w-full rounded border border-border bg-background px-1 text-center text-[11px] outline-none"
        defaultValue={data.name}
        name="name"
        onBlur={handleBlur}
        onKeyDown={handleKeyDown}
        placeholder="Name"
      />
      <input
        aria-label="Device model"
        className="w-full rounded border border-border bg-background px-1 text-center text-[10px] outline-none"
        defaultValue={data.model}
        name="model"
        onBlur={handleBlur}
        onKeyDown={handleKeyDown}
        placeholder="Model"
      />
    </form>
  );
}

function DeviceNodeView({ id, data, selected }: NodeProps<DeviceNode>) {
  const { editingId, readOnly } = useContext(DiagramContext);
  const connection = useConnection();
  const isDropTarget = connection.inProgress && connection.fromNode.id !== id;

  return (
    <div
      className={cn(
        "group relative flex flex-col items-center gap-0.5 rounded-xl border bg-background px-2 pt-2 pb-1.5 text-center shadow-sm transition-colors",
        selected ? "border-foreground/50" : "border-border",
        isDropTarget && "border-foreground/50 ring-2 ring-foreground/15"
      )}
      data-testid="diagram-device"
      style={{ width: DEVICE_WIDTH }}
    >
      <DeviceIcon size={36} type={data.type} />

      {editingId === id ? (
        <DeviceForm data={data} id={id} />
      ) : (
        <>
          <span className="max-w-full truncate font-medium text-[11px] leading-tight">
            {data.name}
          </span>
          {data.model ? (
            <span className="max-w-full truncate text-[10px] text-muted-foreground leading-tight">
              {data.model}
            </span>
          ) : null}
        </>
      )}

      <Handle
        className={cn(
          "size-3! border-2! border-background! bg-foreground! transition-opacity",
          readOnly
            ? "opacity-0!"
            : selected
              ? "opacity-100"
              : "opacity-0 group-hover:opacity-100"
        )}
        isConnectable={!readOnly}
        position={Position.Bottom}
        type="source"
      />
      {isDropTarget ? (
        <Handle
          id="drop"
          isConnectableStart={false}
          position={Position.Top}
          style={DROP_AREA}
          type="target"
        />
      ) : null}
    </div>
  );
}

function centreOf(node: InternalNode) {
  return {
    x: node.internals.positionAbsolute.x + (node.measured.width ?? 0) / 2,
    y: node.internals.positionAbsolute.y + (node.measured.height ?? 0) / 2,
  };
}

// A straight cable between the middles of two devices; the devices are drawn
// on top, so it seems to start at their edges
function CableEdge({ id, source, target, selected }: EdgeProps) {
  const from = useInternalNode(source);
  const to = useInternalNode(target);

  if (!(from && to)) {
    return null;
  }

  const start = centreOf(from);
  const end = centreOf(to);
  const [path] = getStraightPath({
    sourceX: start.x,
    sourceY: start.y,
    targetX: end.x,
    targetY: end.y,
  });

  return (
    <BaseEdge
      id={id}
      path={path}
      style={{
        stroke: selected ? "var(--foreground)" : "var(--muted-foreground)",
        strokeWidth: selected ? 2.5 : 1.5,
      }}
    />
  );
}

const nodeTypes = { device: DeviceNodeView };
const edgeTypes = { cable: CableEdge };
const DELETE_KEYS = ["Backspace", "Delete"];
const FIT_VIEW = { maxZoom: 1, padding: 0.2 };
const TRANSPARENT = { "--xy-background-color": "transparent" } as CSSProperties;
const PRO_OPTIONS = { hideAttribution: true };

type EditorProps = {
  diagram: NetworkDiagram;
  // Called with the whole diagram after each change (not during a drag)
  onChange?: (diagram: NetworkDiagram) => void;
  readOnly?: boolean;
  className?: string;
};

function Editor({
  diagram,
  onChange,
  readOnly = false,
  className,
}: EditorProps) {
  const { resolvedTheme } = useTheme();
  const { deleteElements, fitView, getEdges, getNodes, screenToFlowPosition } =
    useReactFlow<DeviceNode>();
  const wrapperRef = useRef<HTMLDivElement>(null);
  const [nodes, setNodes] = useState(() => toNodes(diagram));
  const [edges, setEdges] = useState(() => toEdges(diagram));
  const lastDiagram = useRef(JSON.stringify(toDiagram(nodes, edges)));
  const onChangeRef = useRef(onChange);
  onChangeRef.current = onChange;

  useEffect(() => {
    if (nodes.some((node) => node.dragging)) {
      return;
    }

    const next = toDiagram(nodes, edges);
    const json = JSON.stringify(next);

    if (json !== lastDiagram.current) {
      lastDiagram.current = json;
      onChangeRef.current?.(next);
    }
  }, [nodes, edges]);

  const onNodesChange = useCallback(
    (changes: NodeChange<DeviceNode>[]) =>
      setNodes((current) => applyNodeChanges(changes, current)),
    []
  );

  const onEdgesChange = useCallback(
    (changes: EdgeChange[]) =>
      setEdges((current) => applyEdgeChanges(changes, current)),
    []
  );

  const onConnect = useCallback((connection: Connection) => {
    setEdges((current) =>
      isNewCable(connection, current)
        ? [
            ...current,
            {
              id: `${connection.source}->${connection.target}`,
              source: connection.source,
              target: connection.target,
              type: "cable",
            },
          ]
        : current
    );
  }, []);

  const isValidConnection = useCallback(
    (connection: Connection | Edge) => isNewCable(connection, getEdges()),
    [getEdges]
  );

  const addDevice = useCallback(
    (type: string) => {
      const bounds = wrapperRef.current?.getBoundingClientRect();
      const centre = bounds
        ? screenToFlowPosition({
            x: bounds.left + bounds.width / 2,
            y: bounds.top + bounds.height / 2,
          })
        : { x: 0, y: 0 };

      setNodes((current) => {
        const devices = current.map((node) => ({ id: node.id, ...node.data }));
        const device: DeviceNode = {
          data: { model: "", name: nextDeviceName(type, devices), type },
          id: generateUUID(),
          position: freeSpot(
            {
              x: centre.x - DEVICE_WIDTH / 2,
              y: centre.y - DEVICE_HEIGHT / 2,
            },
            current
          ),
          selected: true,
          type: "device",
        };

        return [
          ...current.map((node) => ({ ...node, selected: false })),
          device,
        ];
      });
    },
    [screenToFlowPosition]
  );

  const deleteSelected = useCallback(() => {
    deleteElements({
      edges: getEdges().filter((edge) => edge.selected),
      nodes: getNodes().filter((node) => node.selected),
    });
  }, [deleteElements, getEdges, getNodes]);

  const tidyUp = useCallback(() => {
    const { devices, links } = toDiagram(getNodes(), getEdges());
    const positions = layoutDiagram({
      devices: devices.map(({ x: _x, y: _y, ...device }) => device),
      links,
    });

    setNodes((current) =>
      current.map((node) => ({
        ...node,
        position: positions.get(node.id) ?? node.position,
      }))
    );
    requestAnimationFrame(() => fitView(FIT_VIEW));
  }, [fitView, getEdges, getNodes]);

  const saveImage = useCallback(async () => {
    const devices = getNodes().map((node) => ({
      height: node.measured?.height ?? DEVICE_HEIGHT,
      id: node.id,
      ...node.data,
      width: node.measured?.width ?? DEVICE_WIDTH,
      x: node.position.x,
      y: node.position.y,
    }));

    try {
      await downloadDiagramImage(
        devices,
        toDiagram(getNodes(), getEdges()).links
      );
    } catch {
      toast.error("Couldn't save the diagram as an image. Please try again.");
    }
  }, [getEdges, getNodes]);

  const [editingId, setEditingId] = useState<string | null>(null);
  const stopEditing = useCallback(() => setEditingId(null), []);
  const onNodeDoubleClick = useCallback(
    (_event: MouseEvent, node: DeviceNode) => {
      if (!readOnly) {
        setEditingId(node.id);
      }
    },
    [readOnly]
  );
  const context = useMemo(
    () => ({ editingId, readOnly, stopEditing }),
    [editingId, readOnly, stopEditing]
  );

  const hasSelection =
    nodes.some((node) => node.selected) || edges.some((edge) => edge.selected);

  return (
    <DiagramContext.Provider value={context}>
      <div
        className={cn(
          "h-[380px] w-full overflow-hidden rounded-xl border border-border bg-muted/20",
          className
        )}
        data-testid="network-diagram"
        ref={wrapperRef}
      >
        <ReactFlow
          colorMode={resolvedTheme === "dark" ? "dark" : "light"}
          connectionMode={ConnectionMode.Loose}
          connectionRadius={30}
          deleteKeyCode={readOnly ? null : DELETE_KEYS}
          edges={edges}
          edgesFocusable={!readOnly}
          edgeTypes={edgeTypes}
          elementsSelectable={!readOnly}
          fitView
          fitViewOptions={FIT_VIEW}
          isValidConnection={isValidConnection}
          maxZoom={2}
          minZoom={0.3}
          nodes={nodes}
          nodesConnectable={!readOnly}
          nodesDraggable={!readOnly}
          nodesFocusable={!readOnly}
          nodeTypes={nodeTypes}
          onConnect={onConnect}
          onEdgesChange={onEdgesChange}
          onNodeDoubleClick={onNodeDoubleClick}
          onNodesChange={onNodesChange}
          preventScrolling={false}
          proOptions={PRO_OPTIONS}
          style={TRANSPARENT}
          zoomOnDoubleClick={false}
          zoomOnScroll={false}
        >
          <Background gap={18} size={1} />
          <Controls showInteractive={false} />

          {readOnly ? null : (
            <Panel className="flex gap-1.5" position="top-left">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    className="h-7 gap-1 px-2 text-xs"
                    data-testid="diagram-add-device"
                    size="sm"
                    variant="outline"
                  >
                    <PlusIcon className="size-3.5" />
                    Add device
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="start">
                  {DEVICE_TYPES.map((device) => (
                    <AddDeviceItem
                      key={device.type}
                      label={device.label}
                      onAdd={addDevice}
                      type={device.type}
                    />
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>

              <WithTooltip label="Delete the selected devices and cables">
                <Button
                  className="h-7 gap-1 px-2 text-xs"
                  data-testid="diagram-delete"
                  disabled={!hasSelection}
                  onClick={deleteSelected}
                  size="sm"
                  variant="outline"
                >
                  <Trash2Icon className="size-3.5" />
                  Delete
                </Button>
              </WithTooltip>

              <WithTooltip label="Arrange the devices automatically">
                <Button
                  className="h-7 gap-1 px-2 text-xs"
                  data-testid="diagram-tidy"
                  disabled={nodes.length === 0}
                  onClick={tidyUp}
                  size="sm"
                  variant="outline"
                >
                  <LayoutGridIcon className="size-3.5" />
                  Tidy up
                </Button>
              </WithTooltip>
            </Panel>
          )}

          {nodes.length > 0 ? (
            <Panel position="top-right">
              <WithTooltip label="Download the diagram as a PNG image">
                <Button
                  className="h-7 gap-1 px-2 text-xs"
                  data-testid="diagram-save-image"
                  onClick={saveImage}
                  size="sm"
                  variant="outline"
                >
                  <DownloadIcon className="size-3.5" />
                  Save image
                </Button>
              </WithTooltip>
            </Panel>
          ) : null}

          {readOnly ? null : (
            <Panel
              className="pointer-events-none hidden whitespace-nowrap text-[11px] text-muted-foreground sm:block"
              position="bottom-center"
            >
              {nodes.length === 0
                ? "Add a device to start"
                : "Drag a dot to connect · Double-click to rename"}
            </Panel>
          )}
        </ReactFlow>
      </div>
    </DiagramContext.Provider>
  );
}

function AddDeviceItem({
  label,
  onAdd,
  type,
}: {
  label: string;
  onAdd: (type: string) => void;
  type: string;
}) {
  const handleSelect = useCallback(() => onAdd(type), [onAdd, type]);

  return (
    <DropdownMenuItem className="gap-2 text-xs" onSelect={handleSelect}>
      <DeviceIcon size={18} type={type} />
      {label}
    </DropdownMenuItem>
  );
}

export function NetworkDiagramEditor(props: EditorProps) {
  return (
    <ReactFlowProvider>
      <Editor {...props} />
    </ReactFlowProvider>
  );
}

export function DiagramIcon({ size = 24 }: { size?: number }) {
  return <DeviceIcon size={size} type="router" />;
}
