import { useEffect, useState } from "react";

// Sets cannot be written to storage directly (JSON has no Set), so they travel as arrays.
export const setToArray = (value: Set<string>): unknown => Array.from(value);
export const arrayToSet = (raw: unknown): Set<string> => new Set(Array.isArray(raw) ? (raw as string[]) : []);

// Like useState, but the value is also kept in this browser's localStorage,
// so it survives a page refresh. Storage can be blocked or broken, so every access is guarded.
export function usePersistentState<T>(
    storageKey: string,
    defaultValue: T,
    toStorable: (value: T) => unknown = (value) => value,
    fromStorable: (raw: unknown) => T = (raw) => raw as T,
) {
    const [value, setValue] = useState<T>(() => {
        try {
            const text = localStorage.getItem(storageKey);
            if (text !== null) return fromStorable(JSON.parse(text));
        } catch {
            // broken or blocked storage: start with the default
        }
        return defaultValue;
    });

    useEffect(() => {
        try {
            localStorage.setItem(storageKey, JSON.stringify(toStorable(value)));
        } catch {
            // storage full or blocked: the layout just will not be remembered
        }
    }, [storageKey, value, toStorable]);

    return [value, setValue] as const;
}