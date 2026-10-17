import { useEffect, useRef, useState } from "react";
import "./Workspace.css";
import WidgetFrame, { type Geometry } from "./WidgetFrame";
import type { WidgetConfig, SubsystemConfig, VisualizationType, ParameterConfig } from "../types/telemetry";
import { telemetryConfig } from "../widgets/telemetryConfig";

// Free-form canvas: no grid library. Positions/sizes are raw pixels;
// drag/resize is handled by WidgetFrame via native mouse events.

type WorkspaceProps = {
    sidebarOpen: boolean;
    selectedWidgets: Set<string>;
    setSelectedWidgets: React.Dispatch<React.SetStateAction<Set<string>>>;
};

const DEFAULT_W = 380;
const DEFAULT_H = 260;

// Default spawn point for new widgets - clear of the sidebar overlay (280px).
const SPAWN_X = 420;
const SPAWN_Y = 100;

// Cascade offset applied to consecutive widgets spawning without their
// own saved position, so they don't stack fully on top of each other.
const CASCADE_STEP = 28;
const CASCADE_LIMIT = 8;

// Extra space appended past the furthest widget so there's always
// room to scroll to (and grab) it.
const CANVAS_PADDING = 200;

function Workspace(arg: WorkspaceProps){
    const [geometry, setGeometry] = useState<Record<string, Geometry>>({});
    const [lockedWidgets, setLockedWidgets] = useState<Set<string>>(new Set());

    // Click order, not insertion order - last entry renders on top.
    const [zOrder, setZOrder] = useState<string[]>([]);

    // Cascade slot assigned once per widget, on first spawn without a
    // saved geometry. Tracked as a set of used slots (not a monotonic
    // counter) so a freed slot is reused by the next widget instead of
    // cascading further out.
    const cascadeAssignments = useRef<Map<string, number>>(new Map());
    const usedCascadeSlots = useRef<Set<number>>(new Set());

    function getCascadeIndex(widgetId: string): number {
        if (!cascadeAssignments.current.has(widgetId)) {
            let slot = 0;
            while (usedCascadeSlots.current.has(slot % CASCADE_LIMIT)) {
                slot += 1;
            }
            slot = slot % CASCADE_LIMIT;
            cascadeAssignments.current.set(widgetId, slot);
            usedCascadeSlots.current.add(slot);
        }
        return cascadeAssignments.current.get(widgetId)!;
    }

    function releaseCascadeIndex(widgetId: string) {
        const slot = cascadeAssignments.current.get(widgetId);
        if (slot !== undefined) {
            usedCascadeSlots.current.delete(slot);
            cascadeAssignments.current.delete(widgetId);
        }
    }

    // Per-widget state cleanup lives here, keyed off changes to
    // selectedWidgets, so it fires regardless of WHICH UI action removed
    // the widget (the ✕ button here, or the checkbox in the sidebar,
    // which mutates selectedWidgets directly in App).
    const prevWidgetIds = useRef<Set<string>>(new Set());
    useEffect(() => {
        const current = arg.selectedWidgets;
        for (const id of prevWidgetIds.current) {
            if (!current.has(id)) {
                setGeometry(prev => {
                    if (!(id in prev)) return prev;
                    const next = { ...prev };
                    delete next[id];
                    return next;
                });
                setLockedWidgets(prev => {
                    if (!prev.has(id)) return prev;
                    const next = new Set(prev);
                    next.delete(id);
                    return next;
                });
                setZOrder(prev => prev.filter(existingId => existingId !== id));
                releaseCascadeIndex(id);
            }
        }
        prevWidgetIds.current = new Set(current);
    }, [arg.selectedWidgets]);

    function toggleLock(widgetId: string) {
        setLockedWidgets(prev => {
            const next = new Set(prev);
            if (next.has(widgetId)) {
                next.delete(widgetId);
            } else {
                next.add(widgetId);
            }
            return next;
        });
    }

    function bringToFront(widgetId: string) {
        setZOrder(prev => [...prev.filter(id => id !== widgetId), widgetId]);
    }

    function updateGeometry(widgetId: string, next: Geometry) {
        setGeometry(prev => ({ ...prev, [widgetId]: next }));
    }

    function removeWidget(widgetId: string) {
        // Geometry/lock/z-order/cascade cleanup is handled by the effect
        // above; this only removes the widget from the selection.
        arg.setSelectedWidgets(prev => {
            const next = new Set(prev);
            next.delete(widgetId);
            return next;
        });
    }

    const widgetIds = Array.from(arg.selectedWidgets);

    // Canvas size = bounding box of the furthest widget + padding,
    // rendered as a plain (non-absolute) sizer element so the browser
    // reliably computes scrollWidth/scrollHeight for .workspace.
    let canvasW = 0;
    let canvasH = 0;
    for (const widgetId of widgetIds) {
        const geo = geometry[widgetId];
        if (geo) {
            canvasW = Math.max(canvasW, geo.x + geo.w);
            canvasH = Math.max(canvasH, geo.y + geo.h);
        }
    }
    canvasW += CANVAS_PADDING;
    canvasH += CANVAS_PADDING;

    return(
        <main className={`workspace ${arg.sidebarOpen ? "open" : ""}`}>
            {widgetIds.length === 0 ? (
                <div className="emptyWorkspaceText">
                    Open the menu (+) on the left and select a parameter to display.
                </div>
            ) : (
                <>
                    <div
                        className="workspaceCanvasSizer"
                        style={{ width: canvasW, height: canvasH }}
                    />
                    {widgetIds.map(widgetId => {
                        const [subsystemId, parameterId, visual] = widgetId.split(".");
                        const config: WidgetConfig = {
                            id: widgetId,
                            subsystemId,
                            parameterId,
                            visualization: visual as VisualizationType,
                        };
                        const subsystem = telemetryConfig.find(
                            (s: SubsystemConfig) => s.id === subsystemId);
                        const parameter = subsystem?.parameters.find(
                            (p: ParameterConfig) => p.id === parameterId);

                        const existing = geometry[widgetId];
                        let geo: Geometry;
                        if (existing) {
                            geo = existing;
                        } else {
                            const cascadeIndex = getCascadeIndex(widgetId);
                            geo = {
                                x: SPAWN_X + cascadeIndex * CASCADE_STEP,
                                y: SPAWN_Y + cascadeIndex * CASCADE_STEP,
                                w: DEFAULT_W,
                                h: DEFAULT_H,
                            };
                        }

                        const orderIndex = zOrder.indexOf(widgetId);
                        const zIndex = orderIndex === -1 ? 1 : 10 + orderIndex;

                        return (
                            <WidgetFrame
                                key={widgetId}
                                config={config}
                                title={parameter?.name ?? parameterId}
                                subsystemName={subsystem?.name ?? subsystemId}
                                locked={lockedWidgets.has(widgetId)}
                                geometry={geo}
                                zIndex={zIndex}
                                onGeometryChange={(g) => updateGeometry(widgetId, g)}
                                onFocus={() => bringToFront(widgetId)}
                                onToggleLock={() => toggleLock(widgetId)}
                                onRemove={() => removeWidget(widgetId)}
                            >
                                {visual}
                            </WidgetFrame>
                        );
                    })}
                </>
            )}
        </main>
    );
}

export default Workspace;