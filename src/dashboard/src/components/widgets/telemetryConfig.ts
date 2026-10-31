import type { SubsystemConfig } from "../types/telemetry";
import parameters from "../../../../telemetry_server/parameters_catalog.json";

export const telemetryConfig = parameters.subsystems as SubsystemConfig[];