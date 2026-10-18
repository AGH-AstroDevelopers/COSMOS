import { useRef } from "react";
import type { WidgetConfig } from "../types/telemetry";
import "./Workspace.css"

// Custom drag/resize on native mouse events - no external library.
// Positions are raw pixels, no grid snapping, no collision handling.
//
// Horizontal vs vertical bounds are asymmetric on purpose:
// - x: clamped to viewport width - the dashboard doesn't scroll
//   sideways, so anything past the right edge would be unreachable.
// - y: only clamped to >= 0 - .workspace scrolls vertically, so
//   widgets are free to extend downward.

export type Geometry = { x: number; y: number; w: number; h: number };

type ResizeDir = "n" | "s" | "e" | "w" | "ne" | "nw" | "se" | "sw";

type WidgetFrameProps = {
    config: WidgetConfig;
    title: string;
    subsystemName: string;
    children: React.ReactNode;
    locked: boolean;
    geometry: Geometry;
    zIndex: number;
    onGeometryChange: (g: Geometry) => void;
    onFocus: () => void;
    onToggleLock: () => void;
    onRemove: () => void;
};

const MIN_W = 160;
const MIN_H = 120;

const RESIZE_HANDLES: ResizeDir[] = ["n", "s", "e", "w", "ne", "nw", "se", "sw"];

function WidgetFrame(arg: WidgetFrameProps){
    // Refs, not state - in-progress drag/resize data doesn't need to
    // trigger its own re-render (onGeometryChange already does).
    const dragStart = useRef<{ mouseX: number; mouseY: number; origX: number; origY: number } | null>(null);
    const resizeStart = useRef<{ dir: ResizeDir; mouseX: number; mouseY: number; orig: Geometry } | null>(null);

    // Safety net: if the window loses focus mid-drag (mouse released
    // outside the browser, alt-tab, devtools), mouseup may never reach
    // document, leaving the drag stuck. Force-end on blur.
    function handleWindowBlur() {
        if (dragStart.current) handleDragEnd();
        if (resizeStart.current) handleResizeEnd();
    }

    function handleTileMouseDown(e: React.MouseEvent) {
        if (arg.locked) return;

        const target = e.target as HTMLElement;
        if (target.closest(".widgetHeaderActions")) return;

        // Prevents native text selection / image drag from stealing mousemove events mid-drag.
        e.preventDefault();

        arg.onFocus();

        dragStart.current = {
            mouseX: e.clientX,
            mouseY: e.clientY,
            origX: arg.geometry.x,
            origY: arg.geometry.y,
        };
        document.addEventListener("mousemove", handleDragMove);
        document.addEventListener("mouseup", handleDragEnd);
        window.addEventListener("blur", handleWindowBlur);
    }

    function handleDragMove(e: MouseEvent) {
        const start = dragStart.current;
        if (!start) return;
        const dx = e.clientX - start.mouseX;
        const dy = e.clientY - start.mouseY;

        const maxX = Math.max(0, window.innerWidth - arg.geometry.w);

        arg.onGeometryChange({
            ...arg.geometry,
            x: Math.min(maxX, Math.max(0, start.origX + dx)),
            y: Math.max(0, start.origY + dy),
        });
    }

    function handleDragEnd() {
        dragStart.current = null;
        document.removeEventListener("mousemove", handleDragMove);
        document.removeEventListener("mouseup", handleDragEnd);
        window.removeEventListener("blur", handleWindowBlur);
    }

    function handleResizeMouseDown(e: React.MouseEvent, dir: ResizeDir) {
        e.stopPropagation(); // don't also trigger tile drag
        if (arg.locked) return;
        e.preventDefault();

        arg.onFocus();

        resizeStart.current = {
            dir,
            mouseX: e.clientX,
            mouseY: e.clientY,
            orig: { ...arg.geometry },
        };
        document.addEventListener("mousemove", handleResizeMove);
        document.addEventListener("mouseup", handleResizeEnd);
        window.addEventListener("blur", handleWindowBlur);
    }

    function handleResizeMove(e: MouseEvent) {
        const start = resizeStart.current;
        if (!start) return;
        const dx = e.clientX - start.mouseX;
        const dy = e.clientY - start.mouseY;
        let { x, y, w, h } = start.orig;

        // "e": x stays fixed, so available width is measured from it.
        if (start.dir.includes("e")) {
            const maxW = Math.max(MIN_W, window.innerWidth - start.orig.x);
            w = Math.min(maxW, Math.max(MIN_W, start.orig.w + dx));
        }
        // "s": unbounded, .workspace scrolls to reach it.
        if (start.dir.includes("s")) h = Math.max(MIN_H, start.orig.h + dy);

        // "w"/"n": resizing from the near edge also shifts position,
        // since the opposite edge must stay put.
        if (start.dir.includes("w")) {
            w = Math.max(MIN_W, start.orig.w - dx);
            x = Math.max(0, start.orig.x + (start.orig.w - w));
        }
        if (start.dir.includes("n")) {
            h = Math.max(MIN_H, start.orig.h - dy);
            y = Math.max(0, start.orig.y + (start.orig.h - h));
        }

        arg.onGeometryChange({ x, y, w, h });
    }

    function handleResizeEnd() {
        resizeStart.current = null;
        document.removeEventListener("mousemove", handleResizeMove);
        document.removeEventListener("mouseup", handleResizeEnd);
        window.removeEventListener("blur", handleWindowBlur);
    }

    return(
        <div
            className={`widgetFrame ${arg.locked ? "locked" : ""}`}
            style={{
                position: "absolute",
                left: arg.geometry.x,
                top: arg.geometry.y,
                width: arg.geometry.w,
                height: arg.geometry.h,
                zIndex: arg.zIndex,
            }}
            onMouseDown={handleTileMouseDown}
        >
            <div className="widgetHeader">
                <div className="widgetTitle">
                    <div className="parameterName">
                        {arg.title}
                    </div>
                    <div className="subsystemName">
                        {arg.subsystemName}
                    </div>
                </div>
                <div className="widgetHeaderActions">
                    <button onClick={arg.onToggleLock}> {arg.locked ? "🔒" :  "🔓"} </button>
                    <button onClick={arg.onRemove}>✕</button>
                </div>
            </div>

            <div className="widgetFrameBody">
                {arg.children}
            </div>

            {!arg.locked && RESIZE_HANDLES.map(dir => (
                <div
                    key={dir}
                    className={`resizeHandle resizeHandle-${dir}`}
                    onMouseDown={(e) => handleResizeMouseDown(e, dir)}
                />
            ))}
        </div>
    );
}
export default WidgetFrame;