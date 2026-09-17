I will unify and polish the entire dashboard into a cohesive, executive-grade design system. 

Here is what will be improved across all dashboard components:
1. **Visual Foundation & Theme Engine (`dashboard-theme.ts`)**: Unified chart palettes, shared Recharts tooltips with glassmorphic styling, standard bar radii, and gradient definitions.
2. **Executive KPI Sparkline Cards (`sparkline-kpi-card.tsx`)**: Replaced rigid SVGs with smooth cubic-bezier gradient sparklines, elevated cards with subtle ambient glow, large tabular numbers, and clean delta badges.
3. **Seasonal Wave Velocity Cockpit (`executive-cards.tsx`)**: Replaced raw text dumps with institutional milestone cards (T1 Rentrée, T2 Mi-parcours, T3 Clôture) featuring dual-layer collection meters, 2×2 metric grids, and status pills.
4. **Contextual Insights Rail (`insights-rail.tsx`)**: Upgraded the AI Copilot card with a gradient aura border, transformed the circular recovery gauge into a high-definition ring, and refined the priority debtor relance queue with direct action triggers.
5. **Flow Pipeline & Operating Rhythm (`recovery-funnel-card.tsx`, `weekly-operating-rhythm.tsx`)**: Transformed the recovery funnel into a connected conversion pipeline and elevated the Algerian school-week rhythm chart with stacked methods and day-by-day totals.
6. **Operational Calendar (`dashboard-calendar.tsx`)**: Polished month navigation, clean day cells with multi-event indicator dots, and a daily activity stream with time badges, category chips, and delete/manage capabilities.
7. **Analytics & Diagnostic Hub (`analytics-tab.tsx`, `stat-strip.tsx`, `mix-cards.tsx`, `operational-query-console.tsx`, `cross-risk-card.tsx`, `pivot-matrix-card.tsx`, `debtors-pareto-card.tsx`, `aging-composition-card.tsx`, `yoy-comparison-card.tsx`, `analytics-slicers.tsx`)**: Integrated segmented navigation, streamlined query console, and unified all tables and charts.
8. **Drill-down Modal & Selector (`see-details-modal.tsx`, `academic-year-selector.tsx`, `overview-tab.tsx`, `dashboard-page.tsx`)**: Cohesive typography, unified margins, and consistent visual hierarchy throughout.

---

### Step 1: Upgrading `dashboard-theme.ts`

```typescript
// ============================================================================
// FILE: elimtiyaz-desktop/src/shared/ui/dashboard-theme.ts
// ============================================================================

/**
 * DASHBOARD_THEME — Unified design tokens and styling configuration for
 * dashboard analytics and Recharts visualizations.
 *
 * Provides single-source-of-truth tokens for chart strokes, fills, tooltips,
 * axis typography, and ambient card glows.
 */

function token(name: string, fallback: string): string {
  try {
    if (typeof document === "undefined") return fallback;
    const v = getComputedStyle(document.documentElement)
      .getPropertyValue(name)
      .trim();
    return v || fallback;
  } catch {
    return fallback;
  }
}

/** Palette for chart strokes/fills — mirrors index.css brand & status tokens */
export const chartPalette = {
  primary: token("--brand-blue", "#349bd4"),
  primaryDeep: token("--brand-blue-deep", "#216d9b"),
  primaryLight: token("--brand-blue-light", "#52b6eb"),
  cyan: token("--brand-cyan", "#3dd6d0"),
  violet: token("--brand-violet", "#8b5cf6"),
  gold: token("--brand-gold", "#eab308"),
  coral: token("--brand-coral", "#f43f5e"),
  slate: token("--brand-slate", "#3b464c"),
  success: token("--status-success", "#10b981"),
  danger: token("--status-danger", "#ef4444"),
  warning: token("--status-warning", "#f59e0b"),
  info: token("--status-info", "#0ea5e9"),
};

/** Shared Recharts styling configuration */
export const DASHBOARD_THEME = {
  gridStroke: "rgba(255, 255, 255, 0.06)",
  axisTick: {
    fill: "hsl(var(--muted-foreground))",
    fontSize: 11,
    fontFamily: "JetBrains Mono, ui-monospace, monospace",
    letterSpacing: "-0.02em",
  } as const,
  tooltipStyle: {
    backgroundColor: "var(--surface-elevated, #181d30)",
    border: "1px solid hsl(var(--border) / 0.8)",
    borderRadius: "10px",
    color: "var(--foreground-bright, #f8fafc)",
    fontSize: "12px",
    padding: "8px 12px",
    boxShadow:
      "0 12px 28px -4px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05)",
    backdropFilter: "blur(12px)",
  } as const,
  barRadius: [4, 4, 0, 0] as [number, number, number, number],
  horizontalBarRadius: [0, 4, 4, 0] as [number, number, number, number],
};
```

---

### Step 2: Redesigning `SparklineKpiCard` with Smooth Bezier Sparklines

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/sparkline-kpi-card.tsx
// ============================================================================

/**
 * SparklineKpiCard — Executive KPI Tile with High-Definition Bezier Sparkline.
 *
 * Combines crisp typographic hierarchy, a subtle ambient top border,
 * a formatted trend delta pill, and an area-gradient sparkline.
 */

import { ArrowUpRight, ArrowDownRight, Minus } from "lucide-react";
import { Card, CardContent } from "../../../shared/ui/card";
import { cn } from "../../../shared/ui/cn";

export type SparklineTone = "primary" | "success" | "danger" | "warning";

const STROKE_BY_TONE: Record<SparklineTone, string> = {
  primary: "#349bd4",
  success: "#10b981",
  danger: "#ef4444",
  warning: "#f59e0b",
};

export interface SparklineKpiCardProps {
  label: string;
  value: string;
  subValue?: string;
  deltaPercent?: number;
  deltaPeriod?: string;
  trend?: number[];
  tone?: SparklineTone;
  onClick?: () => void;
  gradientKey?: string;
}

/**
 * Generates a smooth cubic-bezier SVG path string through an array of points.
 */
function generateSmoothSvgPath(
  points: Array<{ x: number; y: number }>,
): string {
  if (points.length === 0) return "";
  if (points.length === 1) return `M ${points[0].x} ${points[0].y}`;
  if (points.length === 2) {
    return `M ${points[0].x} ${points[0].y} L ${points[1].x} ${points[1].y}`;
  }

  let d = `M ${points[0].x.toFixed(1)} ${points[0].y.toFixed(1)}`;
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[i === 0 ? 0 : i - 1];
    const p1 = points[i];
    const p2 = points[i + 1];
    const p3 = points[i + 2] ?? p2;

    const cp1x = p1.x + (p2.x - p0.x) / 6;
    const cp1y = p1.y + (p2.y - p0.y) / 6;
    const cp2x = p2.x - (p3.x - p1.x) / 6;
    const cp2y = p2.y - (p3.y - p1.y) / 6;

    d += ` C ${cp1x.toFixed(1)} ${cp1y.toFixed(1)}, ${cp2x.toFixed(1)} ${cp2y.toFixed(1)}, ${p2.x.toFixed(1)} ${p2.y.toFixed(1)}`;
  }
  return d;
}

export function SparklineKpiCard({
  label,
  value,
  subValue,
  deltaPercent,
  deltaPeriod = "vs période préc.",
  trend,
  tone = "primary",
  onClick,
  gradientKey,
}: SparklineKpiCardProps) {
  const hasDelta =
    typeof deltaPercent === "number" && Number.isFinite(deltaPercent);
  const isPositive = hasDelta && (deltaPercent as number) > 0;
  const isZero = hasDelta && deltaPercent === 0;
  const color = STROKE_BY_TONE[tone];
  const hasSparkline = Array.isArray(trend) && trend.length >= 2;

  // Normalized geometry in a 92x36 viewBox
  const width = 92;
  const height = 36;
  let strokePath = "";
  let areaPath = "";

  if (hasSparkline && trend) {
    const min = Math.min(...trend);
    const max = Math.max(...trend);
    const range = max - min || 1;

    const points = trend.map((val, i) => {
      const x = (i / (trend.length - 1)) * width;
      const y = height - ((val - min) / range) * (height - 10) - 5;
      return { x, y };
    });

    strokePath = generateSmoothSvgPath(points);
    areaPath = `${strokePath} L ${width} ${height} L 0 ${height} Z`;
  }

  const gradientId = `spark-grad-${(gradientKey ?? label)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")}`;

  return (
    <Card
      onClick={onClick}
      className={cn(
        "group relative overflow-hidden rounded-xl border border-border/70 bg-surface-panel p-0 transition-all duration-200",
        onClick &&
          "cursor-pointer hover:border-primary/40 hover:bg-surface-elevated/50 hover:shadow-lg hover:shadow-black/20",
      )}
    >
      {/* Subtle top indicator bar with tone accent */}
      <div
        className="h-[2px] w-full"
        style={{
          background: `linear-gradient(90deg, ${color} 0%, transparent 80%)`,
        }}
      />

      <CardContent className="p-4 flex items-end justify-between gap-3">
        <div className="space-y-1.5 min-w-0 flex-1">
          <div className="flex items-center gap-1.5">
            <span
              className="h-1.5 w-1.5 rounded-full shrink-0"
              style={{ backgroundColor: color }}
            />
            <p className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground truncate">
              {label}
            </p>
          </div>

          <div className="flex items-baseline gap-2 flex-wrap">
            <span className="text-2xl font-bold font-mono tracking-tight text-foreground tabular-nums">
              {value}
            </span>
            {subValue && (
              <span className="text-xs font-mono text-muted-foreground tabular-nums">
                {subValue}
              </span>
            )}
          </div>

          {hasDelta ? (
            <div className="flex items-center gap-1.5 pt-0.5">
              <span
                className={cn(
                  "inline-flex items-center text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded-md",
                  isZero
                    ? "bg-muted text-muted-foreground"
                    : isPositive
                      ? "bg-status-success/15 text-status-success"
                      : "bg-status-danger/15 text-status-danger",
                )}
              >
                {isZero ? (
                  <Minus className="h-2.5 w-2.5 mr-0.5" />
                ) : isPositive ? (
                  <ArrowUpRight className="h-2.5 w-2.5 mr-0.5" />
                ) : (
                  <ArrowDownRight className="h-2.5 w-2.5 mr-0.5" />
                )}
                {Math.abs(deltaPercent as number)}%
              </span>
              <span className="text-[11px] text-muted-foreground truncate">
                {deltaPeriod}
              </span>
            </div>
          ) : (
            <div className="text-[11px] text-muted-foreground/60 h-4">&nbsp;</div>
          )}
        </div>

        {hasSparkline && (
          <div className="w-[92px] h-[36px] shrink-0 mb-1" aria-hidden="true">
            <svg width={width} height={height} className="overflow-visible">
              <defs>
                <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={color} stopOpacity={0.35} />
                  <stop offset="100%" stopColor={color} stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <path d={areaPath} fill={`url(#${gradientId})`} />
              <path
                d={strokePath}
                fill="none"
                stroke={color}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

---

### Step 3: Upgrading the Seasonal Wave Velocity & Executive Dashboard (`executive-cards.tsx`)

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/executive-cards.tsx
// ============================================================================

import { useMemo } from "react";
import {
  Waves,
  Percent,
  PhoneCall,
  Users,
  Bus,
  Stethoscope,
  Scale,
  Radar,
  AlertTriangle,
  TrendingDown,
  Calendar,
  CheckCircle2,
  Clock,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../../shared/ui/card";
import { formatDzd, formatDzdPlain } from "../../../../core/format/currency";
import { PAYMENT_CATEGORY_LABELS_FR } from "../../../../domain/model/payment";
import type { Payment } from "../../../../domain/model/payment";
import type { Installment } from "../../../../domain/model/payment";
import type { LedgerEntry } from "../../../../domain/model/ledger";
import type { Student } from "../../../../domain/model/student";
import type { Parent } from "../../../../domain/model/parent";
import type { AcademicClass } from "../../../../domain/model/academic";
import {
  deriveTrancheWaves,
  deriveDiscountErosion,
  deriveDebtTriage,
  deriveFamilyConcentration,
  deriveTransportYield,
  deriveServiceYield,
  deriveEnrollmentDynamics,
  deriveTripleRiskSummary,
  type TrancheWave,
  type DebtTriage,
  type FamilyConcentration,
  type TransportYield,
  type EnrollmentDynamics,
} from "./executive-statistics";
import type { StudentRiskProfile } from "./operational-query-engine";
import { TRANSPORT_DESTINATION_LABELS_FR } from "../../../../domain/model/parent";

const WAVE_TITLES: Record<number, { title: string; subtitle: string }> = {
  1: { title: "Tranche 1 (T1)", subtitle: "Rentrée & Inscription (Sept)" },
  2: { title: "Tranche 2 (T2)", subtitle: "Mi-parcours scolaire (Déc)" },
  3: { title: "Tranche 3 (T3)", subtitle: "Clôture de scolarité (Mars)" },
};

export function WaveVelocityCard({
  waves,
  variant = "full",
}: {
  waves: TrancheWave[];
  variant?: "full" | "hero";
}) {
  const tuition = waves.filter((w) => w.category === "tuition");
  const others = waves.filter((w) => w.category !== "tuition");
  const totalDue = waves.reduce((s, w) => s + w.dueTotal, 0);
  const totalPaid = waves.reduce((s, w) => s + w.paidTotal, 0);
  const totalRemaining = waves.reduce((s, w) => s + w.remainingTotal, 0);
  const globalPct = totalDue > 0 ? Math.round((totalPaid / totalDue) * 100) : 0;

  return (
    <Card
      className="border-border/70 bg-surface-panel shadow-sm flex flex-col"
      data-testid="wave-velocity-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between gap-3 flex-wrap">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Waves className="h-4 w-4 text-primary" />
            Vélocité de Recouvrement par Vague Saisonnière
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Échéancier réel par tranche (Septembre · Décembre · Mars)
          </CardDescription>
        </div>

        {waves.length > 0 && (
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/20 font-semibold">
              {globalPct}% collecté global
            </span>
            <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-status-danger/10 text-status-danger border border-status-danger/20 font-semibold">
              {formatDzd(totalRemaining, { compact: true })} restant
            </span>
          </div>
        )}
      </CardHeader>

      <CardContent className="p-4 space-y-4 flex-1">
        {waves.length === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-10"
            data-testid="wave-velocity-empty"
          >
            Aucune tranche facturée sur la période sélectionnée.
          </p>
        ) : (
          <>
            {/* The 3 Main Tuition Waves */}
            <div
              className="grid grid-cols-1 md:grid-cols-3 gap-3.5"
              data-testid="wave-tuition-grid"
            >
              {tuition.map((w) => {
                const isOverdue = w.phase === "overdue";
                const isComplete = w.collectedPct >= 95;
                const statusTone = isComplete
                  ? "success"
                  : isOverdue
                    ? "danger"
                    : "info";

                return (
                  <div
                    key={`${w.category}-${w.wave}`}
                    className="rounded-xl border border-border/80 bg-surface-elevated/30 p-3.5 space-y-3 transition-all hover:border-border hover:bg-surface-elevated/60"
                    data-testid={`wave-meter-${w.wave}`}
                  >
                    {/* Header */}
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <h4 className="text-xs font-bold text-foreground">
                          {WAVE_TITLES[w.wave]?.title ?? `Tranche ${w.wave}`}
                        </h4>
                        <p className="text-[11px] text-muted-foreground">
                          {WAVE_TITLES[w.wave]?.subtitle ?? "Scolarité"}
                        </p>
                      </div>
                      <span
                        className={`inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full border ${
                          statusTone === "success"
                            ? "bg-status-success/15 text-status-success border-status-success/30"
                            : statusTone === "danger"
                              ? "bg-status-danger/15 text-status-danger border-status-danger/30"
                              : "bg-status-info/15 text-status-info border-status-info/30"
                        }`}
                      >
                        {statusTone === "success" ? (
                          <CheckCircle2 className="h-2.5 w-2.5" />
                        ) : statusTone === "danger" ? (
                          <AlertTriangle className="h-2.5 w-2.5" />
                        ) : (
                          <Clock className="h-2.5 w-2.5" />
                        )}
                        {isComplete
                          ? "Clôturée"
                          : isOverdue
                            ? "En retard"
                            : "En cours"}
                      </span>
                    </div>

                    {/* Progress Bar & Rate */}
                    <div className="space-y-1.5">
                      <div className="flex items-baseline justify-between">
                        <span className="text-xl font-bold font-mono text-foreground tabular-nums">
                          {w.collectedPct}%
                        </span>
                        <span className="text-xs font-mono text-muted-foreground">
                          {w.paidCount}/{w.installmentCount} dossiers
                        </span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-muted/60 overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all duration-500"
                          style={{
                            width: `${Math.min(100, w.collectedPct)}%`,
                            backgroundColor:
                              statusTone === "success"
                                ? "var(--status-success, #10b981)"
                                : statusTone === "danger"
                                  ? "var(--status-danger, #ef4444)"
                                  : "var(--brand-blue, #349bd4)",
                          }}
                        />
                      </div>
                    </div>

                    {/* 2x2 Metric Grid */}
                    <div className="grid grid-cols-2 gap-2 pt-1 border-t border-border/40 text-[11px]">
                      <div className="rounded-lg bg-surface-panel/60 p-2 border border-border/40">
                        <span className="text-[10px] uppercase tracking-wider text-muted-foreground block">
                          Facturé
                        </span>
                        <span className="font-mono font-semibold text-foreground">
                          {formatDzdPlain(w.dueTotal)}
                        </span>
                      </div>
                      <div className="rounded-lg bg-surface-panel/60 p-2 border border-border/40">
                        <span className="text-[10px] uppercase tracking-wider text-muted-foreground block">
                          Encaissé
                        </span>
                        <span className="font-mono font-semibold text-status-success">
                          {formatDzdPlain(w.paidTotal)}
                        </span>
                      </div>
                      <div className="rounded-lg bg-surface-panel/60 p-2 border border-border/40">
                        <span className="text-[10px] uppercase tracking-wider text-muted-foreground block">
                          Reste dû
                        </span>
                        <span
                          className={`font-mono font-semibold ${
                            w.remainingTotal > 0
                              ? "text-status-danger"
                              : "text-muted-foreground"
                          }`}
                        >
                          {formatDzdPlain(w.remainingTotal)}
                        </span>
                      </div>
                      <div className="rounded-lg bg-surface-panel/60 p-2 border border-border/40">
                        <span className="text-[10px] uppercase tracking-wider text-muted-foreground block">
                          Familles en retard
                        </span>
                        <span
                          className={`font-mono font-semibold ${
                            w.debtorFamilyCount > 0
                              ? "text-status-warning"
                              : "text-muted-foreground"
                          }`}
                        >
                          {w.debtorFamilyCount} / {w.familyCount}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Other auxiliary waves */}
            {others.length > 0 && variant === "full" && (
              <div
                className="pt-2 border-t border-border/40 space-y-2"
                data-testid="wave-others"
              >
                <span className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground block">
                  Autres Vagues de Facturation (Transport & Services)
                </span>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5">
                  {others.map((w) => (
                    <div
                      key={`${w.category}-${w.wave}`}
                      className="rounded-lg border border-border/60 bg-surface-elevated/20 p-2.5 flex items-center justify-between gap-3 text-xs"
                    >
                      <div className="min-w-0">
                        <p className="font-medium text-foreground truncate">
                          {PAYMENT_CATEGORY_LABELS_FR[w.category] ?? w.category} ·
                          T{w.wave}
                        </p>
                        <p className="text-[10px] font-mono text-muted-foreground">
                          {formatDzd(w.remainingTotal, { compact: true })} restants
                        </p>
                      </div>
                      <span className="font-mono font-bold text-foreground">
                        {w.collectedPct}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}

export function DiscountErosionCard({
  ledger,
}: {
  ledger: readonly LedgerEntry[];
}) {
  const erosion = useMemo(() => deriveDiscountErosion(ledger), [ledger]);

  return (
    <Card
      className="border-border/70 bg-surface-panel h-full flex flex-col justify-between"
      data-testid="discount-erosion-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
          <Percent className="h-4 w-4 text-status-warning" />
          Taux d'Érosion des Remises
        </CardTitle>
        <CardDescription className="text-xs text-muted-foreground">
          {erosion.remiseCount > 0
            ? `${erosion.remiseCount} remises accordées à ${erosion.remiseFamilyCount} familles`
            : "Impact des concessions tarifaires sur les revenus"}
        </CardDescription>
      </CardHeader>

      <CardContent className="p-4 space-y-3.5 flex-1 flex flex-col justify-center">
        {erosion.remiseCount === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-8"
            data-testid="discount-erosion-empty"
          >
            Aucune remise commerciale enregistrée au grand livre.
          </p>
        ) : (
          <>
            <div className="flex items-baseline justify-between">
              <div>
                <span className="text-3xl font-bold font-mono text-foreground tabular-nums">
                  {erosion.erosionPct}%
                </span>
                <span className="text-xs text-muted-foreground block mt-0.5">
                  du tarif catalogue brut concédé en réductions
                </span>
              </div>
              <div className="text-right font-mono">
                <span className="text-sm font-bold text-status-warning">
                  −{formatDzd(erosion.remiseTotal, { compact: true })}
                </span>
                <span className="text-[10px] text-muted-foreground block">
                  remises brutes
                </span>
              </div>
            </div>

            {/* Erosion Gauge */}
            <div className="h-2 w-full rounded-full bg-muted/60 overflow-hidden">
              <div
                className="h-full rounded-full bg-status-warning transition-all"
                style={{ width: `${Math.min(100, erosion.erosionPct)}%` }}
              />
            </div>

            <div className="rounded-lg border border-border/60 bg-surface-elevated/30 p-3 space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Volume catalogue brut</span>
                <span className="font-mono font-semibold">
                  {formatDzdPlain(erosion.stickerTotal)} DA
                </span>
              </div>
              <div className="flex justify-between text-status-warning font-semibold">
                <span>Remises commerciales</span>
                <span className="font-mono">
                  −{formatDzdPlain(erosion.remiseTotal)} DA
                </span>
              </div>
              <div className="flex justify-between border-t border-border/40 pt-1.5 font-bold">
                <span>Net facturé (devis effectifs)</span>
                <span className="font-mono text-foreground">
                  {formatDzdPlain(erosion.grossCharges)} DA
                </span>
              </div>
              <div className="flex justify-between text-[11px] text-muted-foreground">
                <span>Remise moyenne par famille</span>
                <span className="font-mono">
                  {formatDzdPlain(erosion.averageRemise)} DA
                </span>
              </div>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}

export function DebtTriageCard({
  triage,
  parents,
}: {
  triage: DebtTriage;
  parents: readonly Parent[];
}) {
  const parentNameById = useMemo(
    () =>
      new Map(
        parents.map((p) => [
          p.id,
          p.displayName || `${p.firstName} ${p.lastName}`.trim() || p.id,
        ]),
      ),
    [parents],
  );

  const colors: Record<string, string> = {
    not_due: "var(--status-info, #0ea5e9)",
    current: "var(--status-success, #10b981)",
    reminder: "var(--status-warning, #f59e0b)",
    chronic: "var(--status-danger, #ef4444)",
  };

  return (
    <Card
      className="border-border/70 bg-surface-panel h-full flex flex-col justify-between"
      data-testid="debt-triage-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between flex-wrap gap-2">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <PhoneCall className="h-4 w-4 text-status-danger" />
            Triage des Créances & File de Relance
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Ventilation par degré d'urgence et dossiers à traiter en priorité
          </CardDescription>
        </div>

        {triage.totalOutstanding > 0 && (
          <span className="text-xs font-mono font-bold text-status-danger">
            {formatDzd(triage.totalOutstanding, { compact: true })} total
          </span>
        )}
      </CardHeader>

      <CardContent className="p-4 space-y-3.5 flex-1">
        {triage.totalOutstanding === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-8"
            data-testid="debt-triage-empty"
          >
            Toutes les créances sont à jour — aucun dossier en retard.
          </p>
        ) : (
          <>
            {/* The 4 Tiers */}
            <div className="space-y-2" data-testid="debt-triage-buckets">
              {triage.buckets.map((b) => (
                <div key={b.bucket} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="flex items-center gap-1.5 font-medium">
                      <span
                        className="h-2 w-2 rounded-full"
                        style={{ backgroundColor: colors[b.bucket] }}
                      />
                      {b.label}
                    </span>
                    <span className="font-mono text-muted-foreground">
                      <strong className="text-foreground">
                        {formatDzd(b.amount, { compact: true })}
                      </strong>{" "}
                      ({b.familyCount} fam.)
                    </span>
                  </div>
                  <div className="h-1.5 w-full rounded-full bg-muted/60 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{
                        width: `${b.share}%`,
                        backgroundColor: colors[b.bucket],
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>

            {/* Immediate Call List */}
            {triage.callList.length > 0 && (
              <div
                className="rounded-xl border border-status-danger/30 bg-status-danger/5 p-3 space-y-2"
                data-testid="debt-triage-call-list"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-bold text-status-danger uppercase tracking-wider flex items-center gap-1">
                    <AlertTriangle className="h-3.5 w-3.5" />
                    File d'Appel Urgent (&gt; 45 jours)
                  </span>
                  <span className="text-[10px] text-muted-foreground">
                    {triage.callList.length} familles
                  </span>
                </div>

                <div className="space-y-1.5">
                  {triage.callList.slice(0, 4).map((item) => (
                    <div
                      key={item.parentId}
                      className="flex items-center justify-between text-xs py-1 border-b border-border/30 last:border-0"
                    >
                      <span className="font-medium truncate max-w-[170px]">
                        {parentNameById.get(item.parentId) ?? "Famille"}
                      </span>
                      <div className="flex items-center gap-2 font-mono">
                        <span className="text-[10px] text-muted-foreground">
                          {item.worstDaysOverdue}j retard
                        </span>
                        <span className="font-bold text-status-danger">
                          {formatDzdPlain(item.outstanding)} DA
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}

export function FamilyConcentrationCard({
  concentration,
}: {
  concentration: FamilyConcentration;
}) {
  return (
    <Card
      className="border-border/70 bg-surface-panel h-full flex flex-col justify-between"
      data-testid="family-concentration-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
          <Users className="h-4 w-4 text-primary" />
          Concentration du Risque par Foyer
        </CardTitle>
        <CardDescription className="text-xs text-muted-foreground">
          Top {concentration.topFamilies.length} familles représentent{" "}
          <strong className="text-foreground">
            {concentration.topConcentrationPct}%
          </strong>{" "}
          de la dette globale
        </CardDescription>
      </CardHeader>

      <CardContent className="p-4 space-y-3 flex-1 flex flex-col justify-between">
        {concentration.debtorFamilyCount === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-8"
            data-testid="family-concentration-empty"
          >
            Aucune créance familiale enregistrée.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-border/60 text-muted-foreground text-left">
                  <th className="py-2 px-1 font-medium">Famille</th>
                  <th className="py-2 px-1 text-center font-medium">Enfants</th>
                  <th className="py-2 px-1 text-right font-medium">Encours</th>
                  <th className="py-2 px-1 text-right font-medium">Part</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40">
                {concentration.topFamilies.slice(0, 5).map((f) => (
                  <tr key={f.parentId} className="hover:bg-accent/5">
                    <td className="py-2 px-1 font-medium truncate max-w-[140px]">
                      {f.parentName}
                    </td>
                    <td className="py-2 px-1 text-center font-mono">
                      {f.childCount}
                    </td>
                    <td className="py-2 px-1 text-right font-mono font-bold text-status-danger">
                      {formatDzd(f.outstanding, { compact: true })}
                    </td>
                    <td className="py-2 px-1 text-right font-mono text-muted-foreground">
                      {f.shareOfTotalDebt}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function TransportYieldCard({
  transport,
}: {
  transport: TransportYield;
}) {
  return (
    <Card
      className="border-border/70 bg-surface-panel h-full flex flex-col justify-between"
      data-testid="transport-yield-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
          <Bus className="h-4 w-4 text-brand-cyan" />
          Rendement des Tournées Transport
        </CardTitle>
        <CardDescription className="text-xs text-muted-foreground">
          {transport.riders} élèves transportés · {transport.routes.length} circuits
        </CardDescription>
      </CardHeader>

      <CardContent className="p-4 space-y-3 flex-1 flex flex-col justify-between">
        {transport.routes.length === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-8"
            data-testid="transport-yield-empty"
          >
            Aucune ligne de transport active.
          </p>
        ) : (
          <div className="space-y-2">
            {transport.routes.slice(0, 5).map((r) => (
              <div key={r.destination} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-medium truncate max-w-[180px]">
                    {TRANSPORT_DESTINATION_LABELS_FR[r.destination] ??
                      r.destination}
                  </span>
                  <span className="font-mono text-muted-foreground">
                    <strong className="text-foreground">{r.riders}</strong> él. ·{" "}
                    {r.collectedPct}%
                  </span>
                </div>
                <div className="h-1.5 w-full rounded-full bg-muted/60 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-brand-cyan transition-all"
                    style={{ width: `${r.collectedPct}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function ServiceYieldCard({
  services,
}: {
  services: ReturnType<typeof deriveServiceYield>;
}) {
  return (
    <Card
      className="border-border/70 bg-surface-panel h-full flex flex-col justify-between"
      data-testid="service-yield-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
          <Stethoscope className="h-4 w-4 text-brand-violet" />
          Revenus Services Spécialisés
        </CardTitle>
        <CardDescription className="text-xs text-muted-foreground">
          Orthophonie, Psychologie et Activités Annexes
        </CardDescription>
      </CardHeader>

      <CardContent className="p-4 flex-1 flex flex-col justify-center">
        {services.length === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-8"
            data-testid="service-yield-empty"
          >
            Aucun paiement de service enregistré pour le moment.
          </p>
        ) : (
          <div className="space-y-2.5">
            {services.slice(0, 4).map((s) => (
              <div
                key={s.category}
                className="flex items-center justify-between text-xs py-1 border-b border-border/40 last:border-0"
              >
                <div>
                  <span className="font-medium text-foreground block">
                    {s.label}
                  </span>
                  <span className="text-[10px] text-muted-foreground">
                    {s.studentCount} él. suivis · {s.paymentCount} règlements
                  </span>
                </div>
                <span className="font-mono font-bold text-foreground">
                  {formatDzd(s.revenue, { compact: true })}
                </span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function EnrollmentDynamicsCard({
  dynamics,
}: {
  dynamics: EnrollmentDynamics;
}) {
  return (
    <Card
      className="border-border/70 bg-surface-panel h-full flex flex-col justify-between"
      data-testid="enrollment-dynamics-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
          <Scale className="h-4 w-4 text-primary" />
          Dynamique des Effectifs & Fratries
        </CardTitle>
        <CardDescription className="text-xs text-muted-foreground">
          Indice fratrie :{" "}
          <strong className="text-foreground">
            {dynamics.siblingIndex?.toFixed(2) ?? "—"}
          </strong>{" "}
          élèves par famille
        </CardDescription>
      </CardHeader>

      <CardContent className="p-4 space-y-3.5 flex-1 flex flex-col justify-between">
        {dynamics.totalFamilies === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-8"
            data-testid="enrollment-dynamics-empty"
          >
            Aucun élève actif répertorié.
          </p>
        ) : (
          <>
            <div className="grid grid-cols-2 gap-2 text-center text-xs">
              <div className="rounded-lg bg-surface-elevated/40 p-2 border border-border/40">
                <span className="text-[10px] uppercase text-muted-foreground block">
                  Total Élèves
                </span>
                <span className="text-lg font-bold font-mono">
                  {dynamics.totalStudents}
                </span>
              </div>
              <div className="rounded-lg bg-surface-elevated/40 p-2 border border-border/40">
                <span className="text-[10px] uppercase text-muted-foreground block">
                  Foyers Inscrits
                </span>
                <span className="text-lg font-bold font-mono">
                  {dynamics.totalFamilies}
                </span>
              </div>
            </div>

            {/* Distribution */}
            <div className="space-y-1.5" data-testid="family-size-distribution">
              <span className="text-[11px] font-semibold text-muted-foreground block">
                Répartition taille des familles :
              </span>
              <div className="flex gap-1.5">
                {dynamics.familySizes.map((sz) => (
                  <div
                    key={sz.label}
                    className="flex-1 rounded-md bg-surface-elevated/50 p-1.5 text-center border border-border/40"
                  >
                    <span className="text-[10px] font-mono text-muted-foreground block">
                      {sz.label}
                    </span>
                    <span className="text-xs font-bold font-mono text-foreground">
                      {sz.familyCount}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}

export function TripleRiskSummaryCard({
  summary,
  profiles,
}: {
  summary: ReturnType<typeof deriveTripleRiskSummary>;
  profiles: readonly StudentRiskProfile[];
}) {
  const tripleCount = summary.tripleCriticalCount;

  return (
    <Card
      className={`border-border/80 h-full flex flex-col justify-between ${
        tripleCount > 0
          ? "bg-gradient-to-br from-status-danger/10 via-surface-panel to-surface-panel border-status-danger/40"
          : "bg-surface-panel"
      }`}
      data-testid="triple-risk-summary-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
          <Radar className="h-4 w-4 text-status-danger" />
          Radar de Vigilance Multi-Critères
        </CardTitle>
        <CardDescription className="text-xs text-muted-foreground">
          Corrélation directe : Notes + Assiduité + Créance financière
        </CardDescription>
      </CardHeader>

      <CardContent className="p-4 space-y-3.5 flex-1 flex flex-col justify-between">
        <div className="flex items-baseline justify-between">
          <div>
            <span className="text-3xl font-bold font-mono text-status-danger tabular-nums">
              {tripleCount}
            </span>
            <span className="text-xs text-muted-foreground block mt-0.5">
              élèves cumulant le triple risque critique
            </span>
          </div>
          <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-status-danger/20 text-status-danger border border-status-danger/30">
            {summary.tripleCriticalPct}% cohorte
          </span>
        </div>

        <div
          className="grid grid-cols-3 gap-2 text-center text-xs"
          data-testid="triple-risk-counts"
        >
          <div className="rounded-lg bg-surface-elevated/40 p-2 border border-border/40">
            <span className="text-[10px] text-muted-foreground block">
              Moyenne &lt; 10
            </span>
            <span className="text-sm font-bold font-mono text-status-warning">
              {summary.academicAlertCount}
            </span>
          </div>
          <div className="rounded-lg bg-surface-elevated/40 p-2 border border-border/40">
            <span className="text-[10px] text-muted-foreground block">
              Absences ≥ 3
            </span>
            <span className="text-sm font-bold font-mono text-status-warning">
              {summary.attendanceAlertCount}
            </span>
          </div>
          <div className="rounded-lg bg-surface-elevated/40 p-2 border border-border/40">
            <span className="text-[10px] text-muted-foreground block">
              Dette ouverte
            </span>
            <span className="text-sm font-bold font-mono text-status-danger">
              {summary.financialTensionCount}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function ExecutiveDashboard({
  installments,
  ledger,
  students,
  parents,
  classes,
  payments,
  riskProfiles,
  nowEpochMs,
}: {
  installments: readonly Installment[];
  ledger: readonly LedgerEntry[];
  students: readonly Student[];
  parents: readonly Parent[];
  classes: readonly AcademicClass[];
  payments: readonly Payment[];
  riskProfiles: readonly StudentRiskProfile[];
  nowEpochMs: number;
}) {
  const waves = useMemo(
    () => deriveTrancheWaves(installments, nowEpochMs),
    [installments, nowEpochMs],
  );
  const triage = useMemo(
    () => deriveDebtTriage(installments, nowEpochMs),
    [installments, nowEpochMs],
  );
  const concentration = useMemo(
    () =>
      deriveFamilyConcentration({
        installments,
        parents,
        students,
        nowEpochMs,
      }),
    [installments, parents, students, nowEpochMs],
  );
  const transport = useMemo(
    () => deriveTransportYield({ students, installments }),
    [students, installments],
  );
  const services = useMemo(
    () => deriveServiceYield(payments, PAYMENT_CATEGORY_LABELS_FR),
    [payments],
  );
  const dynamics = useMemo(
    () => deriveEnrollmentDynamics({ students, parents, classes }),
    [students, parents, classes],
  );
  const riskSummary = useMemo(
    () => deriveTripleRiskSummary(riskProfiles),
    [riskProfiles],
  );

  return (
    <div className="space-y-4" data-testid="executive-dashboard">
      {/* Row 1: Radar & Wave Hero */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <div className="lg:col-span-4">
          <TripleRiskSummaryCard summary={riskSummary} profiles={riskProfiles} />
        </div>
        <div className="lg:col-span-8">
          <WaveVelocityCard waves={waves} />
        </div>
      </div>

      {/* Row 2: Debt Triage & Discount Erosion */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <div className="lg:col-span-7">
          <DebtTriageCard triage={triage} parents={parents} />
        </div>
        <div className="lg:col-span-5">
          <DiscountErosionCard ledger={ledger} />
        </div>
      </div>

      {/* Row 3: Family Risk Concentration & Enrollment Dynamics */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <div className="lg:col-span-7">
          <FamilyConcentrationCard concentration={concentration} />
        </div>
        <div className="lg:col-span-5">
          <EnrollmentDynamicsCard dynamics={dynamics} />
        </div>
      </div>

      {/* Row 4: Auxiliary Logistics & Services */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <div className="lg:col-span-7">
          <TransportYieldCard transport={transport} />
        </div>
        <div className="lg:col-span-5">
          <ServiceYieldCard services={services} />
        </div>
      </div>
    </div>
  );
}
```

---

### Step 4: Redesigning the Contextual Insights Rail (`insights-rail.tsx`)

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/insights-rail.tsx
// ============================================================================

/**
 * InsightsRail — Zone B Contextual Decision & Real-Time Action Rail.
 *
 * Combines:
 *   1. Smart Copilot actionable decision card with ambient border glow
 *   2. High-definition circular recovery gauge with linear gradient stroke
 *   3. Urgent relance priority list with one-click WhatsApp/Call triggers
 */

import {
  Sparkles,
  ArrowRight,
  Phone,
  Wallet,
  AlertTriangle,
  MessageCircle,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../../../shared/ui/card";
import { Button } from "../../../shared/ui/button";
import { formatDzdPlain, formatDzd } from "../../../core/format/currency";
import type { DebtSummary } from "../../../domain/model/payment";

export interface InsightsRailProps {
  achieved: number;
  outstanding: number;
  overdueFamilies: number;
  deepOverdueFamilies: number;
  topDebtors: readonly DebtSummary[];
  onNavigateAlerts: () => void;
}

export function InsightsRail({
  achieved,
  outstanding,
  overdueFamilies,
  deepOverdueFamilies,
  topDebtors,
  onNavigateAlerts,
}: InsightsRailProps) {
  const totalExpected = achieved + outstanding;
  const percentage =
    totalExpected > 0
      ? Math.min(100, Math.round((achieved / totalExpected) * 100))
      : 0;

  // Circumference for r=38 (2 * pi * 38 ≈ 238.76)
  const circumference = 238.76;
  const strokeDashoffset =
    circumference - (circumference * percentage) / 100;
  const worst = topDebtors[0];

  return (
    <div className="space-y-4">
      {/* 1. Contextual AI Decision Card */}
      <Card className="relative overflow-hidden rounded-xl border border-primary/40 bg-gradient-to-br from-primary/15 via-primary/5 to-surface-panel shadow-sm">
        <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-primary via-brand-cyan to-brand-violet" />
        <CardContent className="p-4 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5 text-primary text-xs font-bold uppercase tracking-wider">
              <Sparkles className="h-4 w-4 shrink-0 animate-pulse" />
              <span>Diagnostic IA en Temps Réel</span>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary/20 text-primary font-semibold">
              Actif
            </span>
          </div>

          {overdueFamilies === 0 ? (
            <p className="text-xs text-foreground leading-relaxed">
              <strong>Recouvrement optimal :</strong> Aucun retard enregistré sur
              la période active. La trésorerie est parfaitement synchronisée.
            </p>
          ) : (
            <div className="space-y-1.5 text-xs text-foreground leading-relaxed">
              <p>
                <strong>{overdueFamilies} familles</strong> cumulent un retard de
                paiement
                {deepOverdueFamilies > 0 && (
                  <>
                    , dont{" "}
                    <strong className="text-status-danger">
                      {deepOverdueFamilies} critiques (&gt; 60 j)
                    </strong>
                  </>
                )}
                .
              </p>
              {worst && (
                <p className="text-[11px] text-muted-foreground">
                  Priorité haute :{" "}
                  <strong className="text-foreground">{worst.parentName}</strong>{" "}
                  ({worst.daysOverdue} j de retard ·{" "}
                  {formatDzdPlain(worst.outstandingAmount)} DA).
                </p>
              )}
            </div>
          )}

          {overdueFamilies > 0 && (
            <Button
              size="sm"
              onClick={onNavigateAlerts}
              className="w-full h-8 text-xs font-semibold gap-1.5 bg-primary hover:bg-primary/90 text-primary-foreground shadow-sm"
            >
              Gérer les Relances Prioritaires
              <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          )}
        </CardContent>
      </Card>

      {/* 2. Recovery Target Radial Gauge */}
      <Card className="rounded-xl border border-border/70 bg-surface-panel p-4 flex items-center gap-4">
        <div className="relative w-20 h-20 shrink-0 flex items-center justify-center">
          <svg
            className="w-full h-full transform -rotate-90"
            viewBox="0 0 100 100"
            aria-hidden="true"
          >
            <circle
              cx="50"
              cy="50"
              r="38"
              stroke="rgba(255, 255, 255, 0.08)"
              strokeWidth="9"
              fill="transparent"
            />
            <circle
              cx="50"
              cy="50"
              r="38"
              stroke="url(#rail-gauge-grad)"
              strokeWidth="9"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              className="transition-all duration-700 ease-out"
            />
            <defs>
              <linearGradient
                id="rail-gauge-grad"
                x1="0%"
                y1="0%"
                x2="100%"
                y2="100%"
              >
                <stop offset="0%" stopColor="#349bd4" />
                <stop offset="100%" stopColor="#10b981" />
              </linearGradient>
            </defs>
          </svg>
          <div className="absolute flex flex-col items-center">
            <span className="text-base font-bold font-mono text-foreground tabular-nums">
              {percentage}%
            </span>
          </div>
        </div>

        <div className="min-w-0 flex-1 space-y-1">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
            Objectif de Recouvrement
          </p>
          <p className="text-sm font-bold font-mono text-foreground truncate">
            {formatDzd(achieved, { compact: true })} encaissés
          </p>
          <p className="text-xs text-muted-foreground font-mono truncate">
            Créances : {formatDzd(outstanding, { compact: true })}
          </p>
          <div className="h-1 w-full rounded-full bg-muted/60 overflow-hidden mt-1">
            <div
              className="h-full bg-status-success rounded-full"
              style={{ width: `${percentage}%` }}
            />
          </div>
        </div>
      </Card>

      {/* 3. Priority Delinquency List */}
      <Card className="rounded-xl border border-border/70 bg-surface-panel shadow-sm">
        <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between">
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <span>À Relancer en Priorité</span>
            {topDebtors.length > 0 && (
              <span className="h-2 w-2 rounded-full bg-status-danger animate-pulse" />
            )}
          </CardTitle>
          <span className="text-[10px] font-mono text-muted-foreground">
            {topDebtors.length} dossiers
          </span>
        </CardHeader>
        <CardContent className="p-3 space-y-2">
          {topDebtors.length === 0 ? (
            <p className="text-xs text-muted-foreground text-center py-4">
              Aucun dossier en attente de relance.
            </p>
          ) : (
            topDebtors.slice(0, 4).map((d) => {
              const cleanPhone = (d.parentPhone || "").replace(/[\s+]/g, "");
              const isUrgent = d.daysOverdue > 45;

              return (
                <div
                  key={d.parentId}
                  className="group flex items-center justify-between gap-2 p-2 rounded-lg border border-border/50 bg-surface-elevated/20 hover:bg-surface-elevated/60 transition-colors"
                >
                  <div className="min-w-0 flex-1">
                    <p className="text-xs font-semibold text-foreground truncate">
                      {d.parentName}
                    </p>
                    <div className="flex items-center gap-2 text-[10px] font-mono text-muted-foreground">
                      <span
                        className={
                          isUrgent ? "text-status-danger font-semibold" : ""
                        }
                      >
                        {d.daysOverdue} j retard
                      </span>
                      <span>·</span>
                      <span className="font-bold text-foreground">
                        {formatDzdPlain(d.outstandingAmount)} DA
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-1 shrink-0">
                    {cleanPhone && (
                      <Button
                        size="sm"
                        variant="ghost"
                        className="h-7 w-7 p-0 text-status-success hover:bg-status-success/15"
                        onClick={() =>
                          window.open(`https://wa.me/${cleanPhone}`, "_blank")
                        }
                        title="WhatsApp"
                      >
                        <MessageCircle className="h-3.5 w-3.5" />
                      </Button>
                    )}
                    <Button
                      size="sm"
                      variant="ghost"
                      className="h-7 w-7 p-0 text-primary hover:bg-primary/15"
                      onClick={onNavigateAlerts}
                      title="Ouvrir le dossier"
                    >
                      <ArrowRight className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </div>
              );
            })
          )}
        </CardContent>
      </Card>
    </div>
  );
}
```

---

### Step 5: Redesigning the Funnel & Operating Rhythm (`recovery-funnel-card.tsx`, `weekly-operating-rhythm.tsx`)

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/recovery-funnel-card.tsx
// ============================================================================

/**
 * RecoveryFunnelCard — Connected Conversion Pipeline.
 *
 * Displays the real delinquency depth progression as a coherent,
 * stepped pipeline with conversion rates and family counts.
 */

import { Filter, ChevronRight } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../shared/ui/card";
import { chartPalette } from "../../../shared/ui/dashboard-theme";
import type { DebtByAgingBucket } from "../../../domain/model/operations";

export interface FunnelStage {
  name: string;
  count: number;
  rateFromPrevious: number;
  color: string;
}

export function deriveRecoveryFunnel(
  debtAging: readonly DebtByAgingBucket[],
): FunnelStage[] {
  const byBucket = new Map(debtAging.map((b) => [b.bucket, b.debtorCount]));
  const total =
    (byBucket.get("0_30") ?? 0) +
    (byBucket.get("31_60") ?? 0) +
    (byBucket.get("61_90") ?? 0) +
    (byBucket.get("91_180") ?? 0) +
    (byBucket.get("180_plus") ?? 0);
  if (total === 0) return [];
  const pct = (n: number) => Math.round((n / total) * 100);
  return [
    {
      name: "Total en Retard",
      count: total,
      rateFromPrevious: 100,
      color: chartPalette.gold,
    },
    {
      name: "Retard Récent (≤ 60 j)",
      count: (byBucket.get("0_30") ?? 0) + (byBucket.get("31_60") ?? 0),
      rateFromPrevious: pct(
        (byBucket.get("0_30") ?? 0) + (byBucket.get("31_60") ?? 0),
      ),
      color: chartPalette.primary,
    },
    {
      name: "Retard Modéré (61–90 j)",
      count: byBucket.get("61_90") ?? 0,
      rateFromPrevious: pct(byBucket.get("61_90") ?? 0),
      color: chartPalette.warning,
    },
    {
      name: "Retard Critique (> 90 j)",
      count:
        (byBucket.get("91_180") ?? 0) + (byBucket.get("180_plus") ?? 0),
      rateFromPrevious: pct(
        (byBucket.get("91_180") ?? 0) + (byBucket.get("180_plus") ?? 0),
      ),
      color: chartPalette.danger,
    },
  ];
}

export function RecoveryFunnelCard({
  stages,
  emptyLabel = "Aucune famille en retard sur la période sélectionnée.",
}: {
  stages: FunnelStage[];
  emptyLabel?: string;
}) {
  const total = stages[0]?.count ?? 0;
  const criticalRate =
    stages.length > 0 && stages[0].count > 0
      ? Math.round((stages[stages.length - 1].count / stages[0].count) * 100)
      : 0;

  return (
    <Card className="h-full border-border/70 bg-surface-panel shadow-sm flex flex-col justify-between">
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Filter className="h-3.5 w-3.5 text-primary" />
            Entonnoir de Dérive des Créances
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Distribution des foyers débiteurs selon l'ancienneté du défaut
          </CardDescription>
        </div>

        {stages.length > 0 && (
          <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-status-danger/10 text-status-danger border border-status-danger/20 font-semibold">
            {criticalRate}% en phase critique
          </span>
        )}
      </CardHeader>

      <CardContent className="p-4 flex-1 flex flex-col justify-center">
        {stages.length === 0 || total === 0 ? (
          <p className="text-xs text-muted-foreground text-center py-8">
            {emptyLabel}
          </p>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 items-stretch">
            {stages.map((stage, idx) => (
              <div
                key={stage.name}
                className="relative rounded-xl border border-border/70 bg-surface-elevated/40 p-3 flex flex-col justify-between space-y-2 hover:border-border transition-all"
              >
                <div className="flex items-center justify-between gap-1">
                  <span className="text-[10px] uppercase font-bold text-muted-foreground truncate">
                    Étape {idx + 1}
                  </span>
                  <span
                    className="text-[10px] font-mono font-bold px-1.5 py-0.2 rounded-full border"
                    style={{
                      color: stage.color,
                      borderColor: `${stage.color}40`,
                      backgroundColor: `${stage.color}15`,
                    }}
                  >
                    {idx === 0 ? "100%" : `${stage.rateFromPrevious}%`}
                  </span>
                </div>

                <div className="space-y-0.5">
                  <span className="text-2xl font-bold font-mono text-foreground tabular-nums block">
                    {stage.count}
                  </span>
                  <span className="text-[11px] text-muted-foreground line-clamp-1">
                    {stage.name}
                  </span>
                </div>

                <div className="h-1.5 w-full rounded-full bg-muted/60 overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${stage.rateFromPrevious}%`,
                      backgroundColor: stage.color,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/weekly-operating-rhythm.tsx
// ============================================================================

/**
 * WeeklyOperatingRhythm — Algerian School-Week Rhythm Chart.
 *
 * Visualizes transaction volume across the Sunday-Thursday school week,
 * stacked cleanly by Cash, Check, and Transfer.
 */

import { useMemo } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";
import { CalendarCheck } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../shared/ui/card";
import { formatDzdPlain, formatDzd } from "../../../core/format/currency";
import {
  DASHBOARD_THEME,
  chartPalette,
} from "../../../shared/ui/dashboard-theme";
import {
  PAYMENT_METHOD_LABELS_FR,
  type Payment,
  type PaymentMethod,
} from "../../../domain/model/payment";

const SCHOOL_WEEK: { key: string; jsDay: number }[] = [
  { key: "Dimanche", jsDay: 0 },
  { key: "Lundi", jsDay: 1 },
  { key: "Mardi", jsDay: 2 },
  { key: "Mercredi", jsDay: 3 },
  { key: "Jeudi", jsDay: 4 },
];

const METHODS: PaymentMethod[] = ["cash", "check", "transfer"];

export interface WeeklyRhythmDatum {
  day: string;
  cash: number;
  check: number;
  transfer: number;
}

export function deriveWeeklyRhythm(
  payments: readonly Payment[],
  range?: { from: string; to: string },
): WeeklyRhythmDatum[] {
  const fromTs = range ? Date.parse(`${range.from}T00:00:00Z`) : null;
  const toTs = range ? Date.parse(`${range.to}T23:59:59Z`) : null;
  const cells = SCHOOL_WEEK.map(() => ({ cash: 0, check: 0, transfer: 0 }));

  for (const p of payments) {
    if (p.status === "refunded") continue;
    const ts = Date.parse(p.collectedAt);
    if (Number.isNaN(ts)) continue;
    if (fromTs !== null && ts < fromTs) continue;
    if (toTs !== null && ts > toTs) continue;
    const jsDay = new Date(ts).getUTCDay();
    const idx = SCHOOL_WEEK.findIndex((d) => d.jsDay === jsDay);
    if (idx === -1) continue;
    cells[idx][p.method] += p.amount;
  }
  return SCHOOL_WEEK.map((d, i) => ({
    day: d.key.slice(0, 3), // e.g. "Dim"
    ...cells[i],
  }));
}

export function WeeklyOperatingRhythm({
  payments,
  range,
}: {
  payments: readonly Payment[];
  range?: { from: string; to: string };
}) {
  const data = useMemo(
    () => deriveWeeklyRhythm(payments, range),
    [payments, range],
  );
  const isEmpty = data.every(
    (d) => d.cash === 0 && d.check === 0 && d.transfer === 0,
  );
  const weeklyTotal = data.reduce(
    (sum, d) => sum + d.cash + d.check + d.transfer,
    0,
  );

  return (
    <Card className="h-full border-border/70 bg-surface-panel shadow-sm flex flex-col justify-between">
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between flex-wrap gap-2">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <CalendarCheck className="h-3.5 w-3.5 text-primary" />
            Rythme d'Encaissement Hebdomadaire
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Volume par jour ouvrable (Dimanche à Jeudi)
          </CardDescription>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono text-muted-foreground">
          {METHODS.map((m) => (
            <span key={m} className="flex items-center gap-1.5">
              <span
                className="h-2 w-2 rounded-full"
                style={{
                  backgroundColor:
                    m === "cash"
                      ? chartPalette.primary
                      : m === "check"
                        ? chartPalette.gold
                        : chartPalette.cyan,
                }}
              />
              <span className="text-foreground">
                {PAYMENT_METHOD_LABELS_FR[m]}
              </span>
            </span>
          ))}
          {weeklyTotal > 0 && (
            <span className="font-bold text-foreground pl-2 border-l border-border/60">
              {formatDzd(weeklyTotal, { compact: true })}
            </span>
          )}
        </div>
      </CardHeader>

      <CardContent className="p-4 flex-1">
        {isEmpty ? (
          <p className="text-xs text-muted-foreground text-center py-8">
            Aucun encaissement sur la période sélectionnée.
          </p>
        ) : (
          <div className="h-[170px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={data}
                margin={{ top: 8, right: 8, bottom: 0, left: -16 }}
              >
                <XAxis
                  dataKey="day"
                  {...DASHBOARD_THEME.axisTick}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  {...DASHBOARD_THEME.axisTick}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v: number) =>
                    `${Math.round(v / 1000)}k`
                  }
                />
                <Tooltip
                  contentStyle={DASHBOARD_THEME.tooltipStyle}
                  formatter={(val: number, name: string) => [
                    `${formatDzdPlain(val)} DZD`,
                    PAYMENT_METHOD_LABELS_FR[name as PaymentMethod] ?? name,
                  ]}
                />
                <Bar
                  dataKey="cash"
                  stackId="a"
                  fill={chartPalette.primary}
                  radius={[0, 0, 0, 0]}
                />
                <Bar
                  dataKey="check"
                  stackId="a"
                  fill={chartPalette.gold}
                  radius={[0, 0, 0, 0]}
                />
                <Bar
                  dataKey="transfer"
                  stackId="a"
                  fill={chartPalette.cyan}
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

---

### Step 6: Upgrading the Dashboard Calendar (`dashboard-calendar.tsx`)

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/dashboard-calendar.tsx
// ============================================================================

/**
 * DashboardCalendar — Embedded operational calendar with unified
 * month-grid and daily activity tracker.
 */

import { useState, useMemo, useEffect } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Plus,
  Trash2,
  Wallet,
  ScrollText,
  Receipt,
  Phone,
  Bell,
  Users,
  Calendar as CalendarIcon,
} from "lucide-react";
import { useRepositories } from "../../app/providers/repository-provider";
import { useToast } from "../../app/providers/toast-provider";
import { useAuth } from "../../app/providers/auth-provider";
import { Button } from "../../shared/ui/button";
import { Badge } from "../../shared/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "../../shared/ui/card";
import { ScrollArea } from "../../shared/ui/scroll-area";
import { StatusChip } from "../../shared/ui/status-chip";
import { CalendarEventCreatorModal } from "./calendar-event-creator-modal";
import { ConfirmModal } from "../../shared/ui/unified-modal";
import {
  CALENDAR_EVENT_KIND_LABELS_FR,
  type CalendarEvent,
  type CalendarEventKind,
} from "../../domain/model/calendar";
import {
  ALERT_PRIORITY_TONE,
  ALERT_PRIORITY_LABELS_FR,
} from "../../domain/model/operations";
import { formatDzdPlain } from "../../core/format/currency";

const WEEKDAYS_FR = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"];
const MONTHS_FR = [
  "Janvier",
  "Février",
  "Mars",
  "Avril",
  "Mai",
  "Juin",
  "Juillet",
  "Août",
  "Septembre",
  "Octobre",
  "Novembre",
  "Décembre",
];

const KIND_ICONS: Record<CalendarEventKind, typeof Wallet> = {
  payment_received: Wallet,
  audit_log: ScrollText,
  expense_event: Receipt,
  follow_up_call: Phone,
  reminder: Bell,
  meeting: Users,
  custom: CalendarIcon,
};

const KIND_TONES: Record<
  CalendarEventKind,
  "success" | "neutral" | "info" | "warning" | "danger"
> = {
  payment_received: "success",
  audit_log: "neutral",
  expense_event: "info",
  follow_up_call: "warning",
  reminder: "info",
  meeting: "neutral",
  custom: "neutral",
};

export function DashboardCalendar() {
  const repos = useRepositories();
  const toast = useToast();
  const { session } = useAuth();
  const today = new Date();
  const [cursor, setCursor] = useState(
    new Date(today.getFullYear(), today.getMonth(), 1),
  );
  const [selectedDate, setSelectedDate] = useState(
    today.toISOString().slice(0, 10),
  );
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [monthEventCounts, setMonthEventCounts] = useState<
    Map<string, number>
  >(new Map());
  const [creatorOpen, setCreatorOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<CalendarEvent | null>(null);

  const yearMonth = `${cursor.getFullYear()}-${String(cursor.getMonth() + 1).padStart(2, "0")}`;

  useEffect(() => {
    const unsub = repos.calendar
      .observeForMonth(yearMonth)
      .subscribe((monthEvents) => {
        const counts = new Map<string, number>();
        for (const e of monthEvents) {
          counts.set(e.date, (counts.get(e.date) ?? 0) + 1);
        }
        setMonthEventCounts(counts);
      });
    return unsub;
  }, [repos.calendar, yearMonth]);

  useEffect(() => {
    const unsub = repos.calendar
      .observeForDate(selectedDate)
      .subscribe((dayEvents) => {
        setEvents(dayEvents);
      });
    return unsub;
  }, [repos.calendar, selectedDate]);

  const monthGrid = useMemo(() => {
    const firstOfMonth = new Date(
      cursor.getFullYear(),
      cursor.getMonth(),
      1,
    );
    const lastOfMonth = new Date(
      cursor.getFullYear(),
      cursor.getMonth() + 1,
      0,
    );
    const startOffset = (firstOfMonth.getDay() + 6) % 7;
    const totalDays = lastOfMonth.getDate();
    const cells: Array<{ date: string | null; day: number }> = [];

    for (let i = 0; i < startOffset; i++) cells.push({ date: null, day: 0 });
    for (let d = 1; d <= totalDays; d++) {
      const dateStr = `${cursor.getFullYear()}-${String(cursor.getMonth() + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
      cells.push({ date: dateStr, day: d });
    }
    while (cells.length % 7 !== 0) cells.push({ date: null, day: 0 });
    return cells;
  }, [cursor]);

  function prevMonth() {
    setCursor(new Date(cursor.getFullYear(), cursor.getMonth() - 1, 1));
  }
  function nextMonth() {
    setCursor(new Date(cursor.getFullYear(), cursor.getMonth() + 1, 1));
  }
  function goToToday() {
    const now = new Date();
    setCursor(new Date(now.getFullYear(), now.getMonth(), 1));
    setSelectedDate(now.toISOString().slice(0, 10));
  }

  async function handleDelete() {
    if (!deleteTarget) return;
    const result = await repos.calendar.delete(deleteTarget.id);
    if (result.ok) {
      toast.showSuccess(
        "Événement supprimé",
        `« ${deleteTarget.title} » a été retiré.`,
      );
    } else {
      toast.showError("Suppression impossible", result.error.userMessage);
    }
    setDeleteTarget(null);
  }

  const canManageEvents = !!session;

  return (
    <Card className="rounded-xl border border-border/70 bg-surface-panel shadow-sm overflow-hidden">
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between">
        <div className="flex items-center gap-2">
          <CalendarIcon className="h-4 w-4 text-primary" />
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Calendrier Opérationnel des Flux & Événements
          </CardTitle>
        </div>

        <div className="flex items-center gap-1.5">
          <Button
            variant="ghost"
            size="sm"
            className="h-7 w-7 p-0"
            onClick={prevMonth}
          >
            <ChevronLeft className="h-3.5 w-3.5" />
          </Button>
          <span className="text-xs font-bold text-foreground px-1">
            {MONTHS_FR[cursor.getMonth()]} {cursor.getFullYear()}
          </span>
          <Button
            variant="ghost"
            size="sm"
            className="h-7 w-7 p-0"
            onClick={nextMonth}
          >
            <ChevronRight className="h-3.5 w-3.5" />
          </Button>
          <Button
            variant="outline"
            size="sm"
            className="h-7 text-xs px-2.5 ml-1 border-primary/30 text-primary"
            onClick={goToToday}
          >
            Aujourd'hui
          </Button>
        </div>
      </CardHeader>

      <CardContent className="p-4 grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Month grid (7 cols) */}
        <div className="lg:col-span-7 space-y-2">
          <div className="grid grid-cols-7 gap-1 text-center">
            {WEEKDAYS_FR.map((d) => (
              <span
                key={d}
                className="text-[10px] font-bold uppercase text-muted-foreground py-1"
              >
                {d}
              </span>
            ))}
          </div>

          <div className="grid grid-cols-7 gap-1">
            {monthGrid.map((cell, i) => {
              if (!cell.date) {
                return (
                  <div
                    key={i}
                    className="h-10 rounded-lg bg-surface-elevated/10"
                  />
                );
              }

              const isSelected = cell.date === selectedDate;
              const isToday =
                cell.date === today.toISOString().slice(0, 10);
              const count = monthEventCounts.get(cell.date) ?? 0;

              return (
                <button
                  key={i}
                  type="button"
                  onClick={() => cell.date && setSelectedDate(cell.date)}
                  className={`relative h-10 rounded-lg text-xs font-mono transition-all flex flex-col items-center justify-center ${
                    isSelected
                      ? "bg-primary text-primary-foreground font-bold shadow-sm ring-1 ring-primary"
                      : isToday
                        ? "bg-primary/10 text-primary font-bold border border-primary/40"
                        : "bg-surface-elevated/30 text-foreground hover:bg-surface-elevated/80 border border-border/30"
                  }`}
                >
                  <span>{cell.day}</span>
                  {count > 0 && (
                    <div className="flex gap-0.5 mt-0.5">
                      {Array.from({ length: Math.min(count, 3) }).map((_, di) => (
                        <span
                          key={di}
                          className={`h-1 w-1 rounded-full ${
                            isSelected ? "bg-white" : "bg-primary"
                          }`}
                        />
                      ))}
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Daily Activity Panel (5 cols) */}
        <div className="lg:col-span-5 flex flex-col rounded-xl border border-border/70 bg-surface-elevated/20 overflow-hidden min-h-[260px]">
          <div className="flex items-center justify-between p-3 border-b border-border/50 bg-surface-panel/40">
            <div>
              <p className="text-xs font-bold text-foreground">
                {selectedDate === today.toISOString().slice(0, 10)
                  ? "Aujourd'hui"
                  : new Date(selectedDate).toLocaleDateString("fr-FR", {
                      weekday: "short",
                      day: "numeric",
                      month: "short",
                    })}
              </p>
              <p className="text-[10px] text-muted-foreground font-mono">
                {events.length} opération(s)
              </p>
            </div>

            {canManageEvents && (
              <Button
                size="sm"
                variant="outline"
                className="h-7 text-xs gap-1 border-primary/40 text-primary"
                onClick={() => setCreatorOpen(true)}
              >
                <Plus className="h-3 w-3" />
                Ajouter
              </Button>
            )}
          </div>

          <ScrollArea className="flex-1 max-h-[260px] p-3">
            {events.length === 0 ? (
              <div className="py-12 text-center text-xs text-muted-foreground">
                Aucune activité enregistrée à cette date.
              </div>
            ) : (
              <div className="space-y-2">
                {events.map((e) => {
                  const Icon = KIND_ICONS[e.kind];
                  const tone = KIND_TONES[e.kind];
                  const isManual =
                    e.kind === "follow_up_call" ||
                    e.kind === "reminder" ||
                    e.kind === "meeting" ||
                    e.kind === "custom";

                  return (
                    <div
                      key={e.id}
                      className="p-2.5 rounded-lg border border-border/50 bg-surface-panel/80 flex items-start gap-2.5 hover:border-border transition-colors"
                    >
                      <div
                        className={`h-7 w-7 rounded-md flex items-center justify-center shrink-0 ${
                          tone === "success"
                            ? "bg-status-success/15 text-status-success"
                            : tone === "warning"
                              ? "bg-status-warning/15 text-status-warning"
                              : tone === "info"
                                ? "bg-status-info/15 text-status-info"
                                : "bg-muted text-muted-foreground"
                        }`}
                      >
                        <Icon className="h-3.5 w-3.5" />
                      </div>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-1.5 flex-wrap">
                          <span className="text-xs font-semibold text-foreground truncate">
                            {e.title}
                          </span>
                          {e.time && (
                            <Badge
                              variant="outline"
                              className="text-[9px] font-mono px-1 py-0"
                            >
                              {e.time}
                            </Badge>
                          )}
                        </div>

                        {e.description && (
                          <p className="text-[11px] text-muted-foreground line-clamp-1 mt-0.5">
                            {e.description}
                          </p>
                        )}

                        <div className="flex items-center gap-2 mt-1 text-[10px]">
                          <span className="font-medium text-muted-foreground">
                            {CALENDAR_EVENT_KIND_LABELS_FR[e.kind]}
                          </span>
                          {e.kind === "payment_received" && (
                            <span className="font-mono font-bold text-status-success">
                              +{formatDzdPlain(e.amount)} DA
                            </span>
                          )}
                        </div>
                      </div>

                      {isManual && canManageEvents && (
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-6 w-6 p-0 text-muted-foreground hover:text-status-danger"
                          onClick={() => setDeleteTarget(e)}
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </ScrollArea>
        </div>
      </CardContent>

      <CalendarEventCreatorModal
        open={creatorOpen}
        onOpenChange={setCreatorOpen}
        presetDate={selectedDate}
      />

      <ConfirmModal
        open={!!deleteTarget}
        onOpenChange={(o) => !o && setDeleteTarget(null)}
        title="Supprimer l'événement ?"
        description={
          deleteTarget ? `« ${deleteTarget.title} » sera retiré du calendrier.` : ""
        }
        destructive
        confirmLabel="Supprimer"
        onConfirm={handleDelete}
      />
    </Card>
  );
}
```

---

### Step 7: Redesigning `OverviewTab` & `DashboardPage`

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/tabs/overview-tab.tsx
// ============================================================================

/**
 * OverviewTab — The 3-Zone Executive Operational Overview.
 *
 * Architecture:
 *   Zone A (8 cols):
 *     Row 1: 4 Sparkline KPI Cards
 *     Row 2: Wave Velocity Milestone Cockpit
 *     Row 3: Recovery Funnel + Weekly Rhythm
 *     Row 4: Operational Calendar
 *   Zone B (4 cols):
 *     Insights Rail (Smart Copilot + Recovery Gauge + Priority Relances)
 */

import { useTranslation } from "react-i18next";
import { SparklineKpiCard } from "../components/sparkline-kpi-card";
import {
  RecoveryFunnelCard,
  deriveRecoveryFunnel,
} from "../components/recovery-funnel-card";
import { WeeklyOperatingRhythm } from "../components/weekly-operating-rhythm";
import { InsightsRail } from "../components/insights-rail";
import { DashboardCalendar } from "../dashboard-calendar";
import { WaveVelocityCard } from "../components/analytics/executive-cards";
import {
  deriveTrancheWaves,
  deriveDebtTriage,
} from "../components/analytics/executive-statistics";
import type {
  DashboardKpi,
  RevenuePoint,
  DebtByAgingBucket,
} from "../../../domain/model/operations";
import type {
  DebtSummary,
  Payment,
  Installment,
} from "../../../domain/model/payment";
import { formatDzd } from "../../../core/format/currency";
import type { Demographics } from "./types";

export interface DashboardData {
  kpis: DashboardKpi | null;
  revenue: RevenuePoint[];
  debtAging: DebtByAgingBucket[];
  demographics: Demographics;
  topDebtors: DebtSummary[];
}

export function OverviewTab({
  data,
  payments,
  installments,
  range,
  onDrillDown,
  onGoToAlerts,
}: {
  data: DashboardData;
  payments: readonly Payment[];
  installments: readonly Installment[];
  range?: { from: string; to: string };
  onDrillDown: (kpi: string) => void;
  onGoToAlerts: () => void;
}) {
  const { t } = useTranslation();
  const { kpis, revenue, debtAging, topDebtors } = data;

  const nowEpochMs = Date.now();
  const waves = deriveTrancheWaves(installments, nowEpochMs);
  const triage = deriveDebtTriage(installments, nowEpochMs);
  const chronicAmount =
    triage.buckets.find((b) => b.bucket === "chronic")?.amount ?? 0;
  const chronicFamilies =
    triage.buckets.find((b) => b.bucket === "chronic")?.familyCount ?? 0;

  const annualRevenue = revenue.reduce((s, r) => s + r.amount, 0);
  const trendSeries =
    revenue.length >= 2 ? revenue.map((r) => r.amount) : undefined;
  const last = revenue.length >= 2 ? revenue[revenue.length - 1] : null;
  const prev = revenue.length >= 2 ? revenue[revenue.length - 2] : null;
  const momDelta =
    last && prev && prev.amount > 0
      ? Math.round(((last.amount - prev.amount) / prev.amount) * 100)
      : undefined;

  const funnelStages = deriveRecoveryFunnel(debtAging);
  const overdueFamilies = debtAging.reduce((s, b) => s + b.debtorCount, 0);
  const deepOverdueFamilies =
    (debtAging.find((b) => b.bucket === "61_90")?.debtorCount ?? 0) +
    (debtAging.find((b) => b.bucket === "91_180")?.debtorCount ?? 0) +
    (debtAging.find((b) => b.bucket === "180_plus")?.debtorCount ?? 0);
  const outstanding = kpis?.outstandingDebt ?? 0;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 pb-8">
      {/* ZONE A: PRIMARY ANALYTICAL STAGE (8 COLS) */}
      <div className="lg:col-span-8 space-y-4">
        {/* Row 1: Sparkline KPIs */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <SparklineKpiCard
            label={t("dashboard.kpi.totalStudents")}
            value={kpis ? String(kpis.totalStudents) : "—"}
            subValue={kpis ? `${kpis.totalParents} foyers` : undefined}
            tone="primary"
            gradientKey="students"
            onClick={() => onDrillDown("students")}
          />
          <SparklineKpiCard
            label={t("dashboard.kpi.monthlyRevenue")}
            value={kpis ? formatDzd(kpis.monthlyRevenue, { compact: true }) : "—"}
            deltaPercent={momDelta}
            trend={trendSeries}
            tone="success"
            gradientKey="monthly-revenue"
            onClick={() => onDrillDown("monthlyRevenue")}
          />
          <SparklineKpiCard
            label={t("dashboard.kpi.outstandingDebt")}
            value={kpis ? formatDzd(outstanding, { compact: true }) : "—"}
            subValue={
              chronicAmount > 0
                ? `${formatDzd(chronicAmount, { compact: true })} urgents (${chronicFamilies} f.)`
                : debtAging.length > 0
                  ? `${overdueFamilies} f. en retard`
                  : undefined
            }
            tone="danger"
            gradientKey="outstanding-debt"
            onClick={() => onDrillDown("outstandingDebt")}
          />
          <SparklineKpiCard
            label="Assiduité Globale"
            value={
              kpis ? `${Math.round(kpis.attendanceRateToday * 100)}%` : "—"
            }
            tone="primary"
            gradientKey="attendance-today"
            onClick={() => onDrillDown("staff")}
          />
        </div>

        {/* Row 2: Milestone Wave Velocity */}
        <WaveVelocityCard waves={waves} variant="hero" />

        {/* Row 3: Funnel & Weekly Rhythm */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <RecoveryFunnelCard stages={funnelStages} />
          <WeeklyOperatingRhythm payments={payments} range={range} />
        </div>

        {/* Row 4: Operational Calendar */}
        <DashboardCalendar />
      </div>

      {/* ZONE B: CONTEXTUAL COMMAND RAIL (4 COLS) */}
      <div className="lg:col-span-4">
        <InsightsRail
          achieved={annualRevenue}
          outstanding={outstanding}
          overdueFamilies={overdueFamilies}
          deepOverdueFamilies={deepOverdueFamilies}
          topDebtors={topDebtors}
          onNavigateAlerts={onGoToAlerts}
        />
      </div>
    </div>
  );
}
```

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/dashboard-page.tsx
// ============================================================================

import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  ChevronRight,
  LayoutDashboard,
  FileText,
  Bell,
  BarChart3,
  Layers,
} from "lucide-react";
import { useRepositories } from "../../app/providers/repository-provider";
import { useAuth } from "../../app/providers/auth-provider";
import type {
  DashboardKpi,
  RevenuePoint,
  DebtByAgingBucket,
} from "../../domain/model/operations";
import type { DebtSummary } from "../../domain/model/payment";
import { PageHeader } from "../../shared/layout/page-header";
import {
  PageTabs,
  PageTabList,
  PageTab,
  PageTabContent,
} from "../../shared/layout/page-tabs";
import { Button } from "../../shared/ui/button";
import { SeeDetailsModal } from "./see-details-modal";
import {
  AcademicYearSelector,
  type AcademicYearRange,
  computeDateRange,
} from "./academic-year-selector";
import { OverviewTab } from "./tabs/overview-tab";
import { AnalyticsTab } from "./tabs/analytics-tab";
import { AlertsTab } from "./tabs/alerts-tab";
import { ReportsTab } from "./tabs/reports-tab";
import {
  type SeeDetailsTab,
  type Demographics,
  AVAILABLE_ACADEMIC_YEARS,
} from "./tabs/types";
import type { Payment, Installment } from "../../domain/model/payment";
import {
  applyAnalyticsFilters,
  installmentsForAcademicYear,
  NO_ANALYTICS_FILTERS,
  previousAcademicYear,
  shiftIsoYearBack,
} from "./components/analytics/analytics-derivations";

type DashboardTab = "overview" | "analytics" | "alerts" | "reports";

interface DashboardData {
  kpis: DashboardKpi | null;
  revenue: RevenuePoint[];
  debtAging: DebtByAgingBucket[];
  demographics: Demographics;
  topDebtors: DebtSummary[];
}

const EMPTY_DEMOGRAPHICS: Demographics = {
  grade: [],
  gender: [],
  age: [],
};

export function DashboardPage() {
  const { t } = useTranslation();
  const repos = useRepositories();
  const { session } = useAuth();

  const [data, setData] = useState<DashboardData>({
    kpis: null,
    revenue: [],
    debtAging: [],
    demographics: EMPTY_DEMOGRAPHICS,
    topDebtors: [],
  });

  const [debtSummaries, setDebtSummaries] = useState<readonly DebtSummary[]>(
    [],
  );
  const [payments, setPayments] = useState<readonly Payment[]>([]);
  const [installments, setInstallments] = useState<readonly Installment[]>([]);
  const [prevRevenue, setPrevRevenue] = useState<RevenuePoint[]>([]);
  const [seeDetailsOpen, setSeeDetailsOpen] = useState(false);
  const [seeDetailsTab, setSeeDetailsTab] = useState<SeeDetailsTab>("revenue");
  const [tab, setTab] = useState<DashboardTab>("overview");
  const [unreadAlerts, setUnreadAlerts] = useState(0);

  const [yearRange, setYearRange] = useState<AcademicYearRange>(() => ({
    academicYear: "2025-2026",
    range: computeDateRange("2025-2026", "ytd"),
    preset: "ytd",
  }));

  // Unified data pipeline
  useEffect(() => {
    void (async () => {
      const [k, rev, debt, demo] = await Promise.all([
        repos.dashboard.kpisForRange(yearRange.academicYear, yearRange.range),
        repos.dashboard.revenueForRange(yearRange.academicYear, yearRange.range),
        repos.dashboard.debtByAgingForRange(
          yearRange.academicYear,
          yearRange.range,
        ),
        repos.dashboard.demographics(),
      ]);
      setData((prev) => ({
        kpis: k.ok ? k.value : null,
        revenue: rev.ok ? rev.value : [],
        debtAging: debt.ok ? debt.value : [],
        demographics: demo.ok ? demo.value : EMPTY_DEMOGRAPHICS,
        topDebtors: prev.topDebtors,
      }));
    })();
  }, [repos.dashboard, yearRange]);

  useEffect(() => {
    const unsub = repos.debt.observeSummary().subscribe((stream) => {
      setDebtSummaries(
        stream
          .filter((d) => d.outstandingAmount > 0)
          .sort((a, b) => b.outstandingAmount - a.outstandingAmount),
      );
    });
    return unsub;
  }, [repos.debt]);

  const topDebtors = useMemo(
    () => debtSummaries.slice(0, 10) as DebtSummary[],
    [debtSummaries],
  );

  useEffect(() => {
    setData((prev) =>
      prev.topDebtors === topDebtors ? prev : { ...prev, topDebtors },
    );
  }, [topDebtors]);

  const prevYearCode = previousAcademicYear(yearRange.academicYear);
  const loadablePrevYear =
    prevYearCode && AVAILABLE_ACADEMIC_YEARS.includes(prevYearCode)
      ? prevYearCode
      : null;

  useEffect(() => {
    const currentRange = yearRange.range;
    if (!loadablePrevYear || !currentRange) {
      setPrevRevenue([]);
      return;
    }
    void (async () => {
      const shifted = {
        from: shiftIsoYearBack(currentRange.from),
        to: shiftIsoYearBack(currentRange.to),
      };
      const prev = await repos.dashboard.revenueForRange(
        loadablePrevYear,
        shifted,
      );
      setPrevRevenue(prev.ok ? prev.value : []);
    })();
  }, [repos.dashboard, loadablePrevYear, yearRange.range]);

  useEffect(() => {
    const unsub = repos.payments.observe().subscribe(setPayments);
    return unsub;
  }, [repos.payments]);

  useEffect(() => {
    const unsub = repos.installments.observe().subscribe(setInstallments);
    return unsub;
  }, [repos.installments]);

  const scopedInstallments = useMemo(
    () => installmentsForAcademicYear(installments, yearRange.academicYear),
    [installments, yearRange.academicYear],
  );

  const rangePayments = useMemo(
    () =>
      applyAnalyticsFilters(payments, yearRange.range, NO_ANALYTICS_FILTERS),
    [payments, yearRange.range],
  );

  useEffect(() => {
    if (!session) return;
    const unsub = repos.notifications
      .observeForSession({ userId: session.userId, role: session.role })
      .subscribe((n) => {
        setUnreadAlerts(n.filter((x) => !x.readAt).length);
      });
    return unsub;
  }, [repos.notifications, session]);

  function openSeeDetails(tab: SeeDetailsTab = "revenue") {
    setSeeDetailsTab(tab);
    setSeeDetailsOpen(true);
  }

  const drillByKpi: Record<string, SeeDetailsTab> = {
    students: "demographics",
    parents: "demographics",
    staff: "demographics",
    monthlyRevenue: "revenue",
    todayRevenue: "revenue",
    outstandingDebt: "debt",
    overdueAlerts: "debt",
    pendingExpenses: "debt",
  };

  const handleKpiClick = (kpi: string) => {
    const target = drillByKpi[kpi];
    if (target) openSeeDetails(target);
  };

  const dataProp = useMemo(() => data, [data]);

  return (
    <div className="flex flex-col h-full bg-surface-background">
      <PageHeader
        title={
          <div className="flex items-center gap-3">
            <span>{t("dashboard.title")}</span>
            <span className="text-xs font-mono font-normal px-2.5 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/20">
              Session {yearRange.academicYear}
            </span>
          </div>
        }
        description="Cockpit institutionnel — pilotage académique, logistique et financier"
        actions={
          <div className="flex items-center gap-2">
            <AcademicYearSelector
              value={yearRange}
              onChange={setYearRange}
              availableYears={AVAILABLE_ACADEMIC_YEARS}
            />
            {tab === "overview" && (
              <Button
                size="sm"
                variant="default"
                className="gap-1 shadow-sm text-xs"
                onClick={() => openSeeDetails("revenue")}
              >
                {t("dashboard.seeDetails")}
                <ChevronRight className="h-4 w-4" />
              </Button>
            )}
          </div>
        }
      />

      <PageTabs
        value={tab}
        onValueChange={(v) => setTab(v as DashboardTab)}
        className="flex-1 flex flex-col px-6 pb-6 min-h-0"
      >
        <PageTabList className="mb-2">
          <PageTab
            value="overview"
            label={t("dashboard.overview")}
            icon={LayoutDashboard}
          />
          <PageTab
            value="analytics"
            label="Analytique & Pilotage"
            icon={BarChart3}
          />
          <PageTab
            value="alerts"
            label={t("dashboard.alerts")}
            icon={Bell}
            count={unreadAlerts}
            countTone="danger"
          />
          <PageTab
            value="reports"
            label={t("dashboard.reports")}
            icon={FileText}
          />
        </PageTabList>

        <PageTabContent value="overview">
          <OverviewTab
            data={dataProp}
            payments={payments}
            installments={scopedInstallments}
            range={yearRange.range}
            onDrillDown={handleKpiClick}
            onGoToAlerts={() => setTab("alerts")}
          />
        </PageTabContent>

        <PageTabContent value="analytics">
          <AnalyticsTab
            revenue={data.revenue}
            prevRevenue={prevRevenue}
            academicYear={yearRange.academicYear}
            prevAcademicYear={loadablePrevYear}
            debtAging={data.debtAging}
            topDebtors={topDebtors}
            debtSummaries={debtSummaries}
            payments={payments}
            installments={scopedInstallments}
            range={yearRange.range}
          />
        </PageTabContent>

        <PageTabContent value="alerts">
          <AlertsTab />
        </PageTabContent>

        <PageTabContent value="reports">
          <ReportsTab />
        </PageTabContent>
      </PageTabs>

      <SeeDetailsModal
        open={seeDetailsOpen}
        onOpenChange={setSeeDetailsOpen}
        initialTab={seeDetailsTab}
        data={dataProp}
        payments={rangePayments}
      />
    </div>
  );
}
```

---

### Step 8: Redesigning `SeeDetailsModal` (`see-details-modal.tsx`)

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/see-details-modal.tsx
// ============================================================================

import { useTranslation } from "react-i18next";
import { useMemo } from "react";
import {
  BarChart3,
  TrendingUp,
  Building2,
  Users,
  AlertCircle,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RTooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  ComposedChart,
  Line,
} from "recharts";
import type {
  DashboardKpi,
  RevenuePoint,
  DebtByAgingBucket,
} from "../../domain/model/operations";
import type { Payment } from "../../domain/model/payment";
import { formatDzd, formatDzdPlain } from "../../core/format/currency";
import {
  AGING_BUCKET_LABELS_FR,
  PAYMENT_CATEGORY_LABELS_FR,
  type PaymentCategory,
  type DebtSummary,
  type AgingBucket,
} from "../../domain/model/payment";
import { UnifiedModal } from "../../shared/ui/unified-modal";
import {
  PageTabs,
  PageTabList,
  PageTab,
  PageTabContent,
} from "../../shared/layout/page-tabs";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../shared/ui/card";
import {
  DASHBOARD_THEME,
  chartPalette,
} from "../../shared/ui/dashboard-theme";
import type { Demographics } from "./tabs/types";

const OPERATIONAL_UNITS: readonly {
  key: string;
  label: string;
  categories: readonly PaymentCategory[];
  color: string;
}[] = [
  {
    key: "scolarite",
    label: "Scolarité (académique)",
    categories: ["tuition", "books", "uniform", "second_apron"],
    color: "#349bd4",
  },
  {
    key: "therapy",
    label: "Thérapie & Accompagnement (Orthophonie / Psy)",
    categories: ["therapy_psychology", "therapy_speech"],
    color: "#eab308",
  },
  {
    key: "clubs",
    label: "Activités & Clubs Parascolaires",
    categories: ["extracurricular"],
    color: "#f43f5e",
  },
  {
    key: "auxiliary",
    label: "Services Auxiliaires (Transport / Cantine)",
    categories: ["transport", "canteen"],
    color: "#10b981",
  },
];

const TRANCHE_PROJECTION_MONTHS: ReadonlyArray<{
  label: string;
  share: number;
}> = [
  { label: "Sep", share: 0.4 },
  { label: "Déc", share: 0.3 },
  { label: "Mar", share: 0.3 },
];

export function deriveTrancheProjection(
  revenue: readonly RevenuePoint[],
  totalExpected: number,
): Array<{ label: string; amount: number; targetProjection: number }> {
  return revenue.map((r) => {
    const rule = TRANCHE_PROJECTION_MONTHS.find((m) => m.label === r.label);
    return {
      label: r.label,
      amount: r.amount,
      targetProjection: rule ? Math.round(totalExpected * rule.share) : 0,
    };
  });
}

function agingSeverity(bucket: AgingBucket): {
  label: string;
  className: string;
} {
  if (bucket === "0_30") {
    return {
      label: "Courant",
      className: "bg-status-success/15 text-status-success border-status-success/30",
    };
  }
  if (bucket === "31_60") {
    return {
      label: "Relance",
      className: "bg-status-warning/15 text-status-warning border-status-warning/30",
    };
  }
  return {
    label: "Critique",
    className: "bg-status-danger/15 text-status-danger border-status-danger/30",
  };
}

export interface DashboardData {
  kpis: DashboardKpi | null;
  revenue: RevenuePoint[];
  debtAging: DebtByAgingBucket[];
  demographics: Demographics;
  topDebtors: DebtSummary[];
}

export function SeeDetailsModal({
  open,
  onOpenChange,
  initialTab = "revenue",
  data,
  payments = [],
}: {
  open: boolean;
  onOpenChange: (o: boolean) => void;
  initialTab?: "revenue" | "departments" | "demographics" | "debt";
  data: DashboardData;
  payments?: readonly Payment[];
}) {
  const { t } = useTranslation();

  const annualRevenue = useMemo(
    () => data.revenue.reduce((s, r) => s + r.amount, 0),
    [data.revenue],
  );
  const outstanding = data.kpis?.outstandingDebt ?? 0;
  const totalExpected = annualRevenue + outstanding;
  const collectionRate =
    totalExpected > 0
      ? Math.round((annualRevenue / totalExpected) * 100)
      : 0;

  const projection = useMemo(
    () =>
      data.kpis
        ? deriveTrancheProjection(data.revenue, totalExpected)
        : data.revenue.map((r) => ({ ...r, targetProjection: 0 })),
    [data.revenue, data.kpis, totalExpected],
  );

  const genderTotal = useMemo(
    () => data.demographics.gender.reduce((s, g) => s + g.count, 0),
    [data.demographics.gender],
  );

  return (
    <UnifiedModal
      open={open}
      onOpenChange={onOpenChange}
      size="2xl"
      variant="dialog"
      icon={BarChart3}
      iconTone="primary"
      title={t("dashboard.seeDetails")}
      description="Analyse approfondie : Recouvrement, Répartition par pôle, Démographie et Débiteurs"
      hideFooter
    >
      <PageTabs defaultValue={initialTab} variant="elevated">
        <PageTabList className="mb-4">
          <PageTab
            value="revenue"
            label={t("dashboard.sections.revenue")}
            icon={TrendingUp}
          />
          <PageTab
            value="departments"
            label={t("dashboard.sections.departments")}
            icon={Building2}
          />
          <PageTab
            value="demographics"
            label={t("dashboard.sections.demographics")}
            icon={Users}
          />
          <PageTab
            value="debt"
            label={t("dashboard.sections.debt")}
            icon={AlertCircle}
          />
        </PageTabList>

        {/* 1. REVENUE SECTION */}
        <PageTabContent value="revenue">
          <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="rounded-xl border border-border/70 bg-surface-elevated/40 p-3.5 space-y-1">
                <span className="text-[10px] font-semibold uppercase text-muted-foreground tracking-wider">
                  Encaissé effectif (PAID)
                </span>
                <p className="text-xl font-mono font-bold text-status-success">
                  {formatDzd(annualRevenue)}
                </p>
                <p className="text-[11px] text-muted-foreground">
                  Fonds collectés et compensés
                </p>
              </div>

              <div className="rounded-xl border border-border/70 bg-surface-elevated/40 p-3.5 space-y-1">
                <span className="text-[10px] font-semibold uppercase text-muted-foreground tracking-wider">
                  Créances restantes
                </span>
                <p className="text-xl font-mono font-bold text-status-danger">
                  {data.kpis ? formatDzd(outstanding) : "—"}
                </p>
                <p className="text-[11px] text-muted-foreground">
                  Engagements à percevoir
                </p>
              </div>

              <div className="rounded-xl border border-border/70 bg-surface-elevated/40 p-3.5 space-y-1">
                <span className="text-[10px] font-semibold uppercase text-muted-foreground tracking-wider">
                  Taux d'Atteinte Annuel
                </span>
                <p className="text-xl font-mono font-bold text-primary">
                  {data.kpis ? `${collectionRate}%` : "—"}
                </p>
                <p className="text-[11px] text-muted-foreground">
                  Encaissé sur total attendu
                </p>
              </div>
            </div>

            <Card className="border-border/70 bg-surface-panel shadow-sm">
              <CardHeader className="py-3 px-4 border-b border-border/50">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Encaissements vs Échéancier Théorique (40% · 30% · 30%)
                </CardTitle>
                <CardDescription className="text-xs text-muted-foreground">
                  Barres pleines : Encaissements réels · Ligne dorée pointillée :
                  Jalons théoriques
                </CardDescription>
              </CardHeader>
              <CardContent className="p-4">
                <div className="h-[260px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <ComposedChart
                      data={projection}
                      margin={{ top: 10, right: 10, bottom: 0, left: -10 }}
                    >
                      <CartesianGrid
                        strokeDasharray="3 3"
                        stroke={DASHBOARD_THEME.gridStroke}
                        vertical={false}
                      />
                      <XAxis
                        dataKey="label"
                        {...DASHBOARD_THEME.axisTick}
                        axisLine={false}
                        tickLine={false}
                      />
                      <YAxis
                        {...DASHBOARD_THEME.axisTick}
                        axisLine={false}
                        tickLine={false}
                        tickFormatter={(v) =>
                          `${Math.round(Number(v) / 1000)}k`
                        }
                      />
                      <RTooltip
                        contentStyle={DASHBOARD_THEME.tooltipStyle}
                        formatter={(v: number, name: string) => [
                          `${formatDzdPlain(v)} DZD`,
                          name === "amount" ? "Encaissé" : "Jalon cible",
                        ]}
                      />
                      <Bar
                        dataKey="amount"
                        name="amount"
                        fill={chartPalette.primary}
                        radius={[4, 4, 0, 0]}
                        barSize={24}
                      />
                      {data.kpis && (
                        <Line
                          type="monotone"
                          dataKey="targetProjection"
                          name="targetProjection"
                          stroke={chartPalette.gold}
                          strokeWidth={2}
                          strokeDasharray="4 4"
                          dot={{ r: 3, fill: chartPalette.gold }}
                        />
                      )}
                    </ComposedChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>
        </PageTabContent>

        {/* 2. DEPARTMENTS SECTION */}
        <PageTabContent value="departments">
          <DepartmentsTab data={data} payments={payments} />
        </PageTabContent>

        {/* 3. DEMOGRAPHICS SECTION */}
        <PageTabContent value="demographics">
          <div className="space-y-4">
            <Card className="border-border/70 bg-surface-panel shadow-sm">
              <CardHeader className="py-3 px-4 border-b border-border/50">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Distribution des Effectifs par Niveau
                </CardTitle>
              </CardHeader>
              <CardContent className="p-4">
                <div className="h-[220px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data.demographics.grade}>
                      <CartesianGrid
                        strokeDasharray="3 3"
                        stroke={DASHBOARD_THEME.gridStroke}
                        vertical={false}
                      />
                      <XAxis
                        dataKey="label"
                        {...DASHBOARD_THEME.axisTick}
                        axisLine={false}
                        tickLine={false}
                        angle={-25}
                        textAnchor="end"
                        height={45}
                      />
                      <YAxis
                        {...DASHBOARD_THEME.axisTick}
                        axisLine={false}
                        tickLine={false}
                        allowDecimals={false}
                      />
                      <RTooltip
                        contentStyle={DASHBOARD_THEME.tooltipStyle}
                        formatter={(v: number) => [`${v} élèves`, "Inscrits"]}
                      />
                      <Bar
                        dataKey="count"
                        fill={chartPalette.primary}
                        radius={[4, 4, 0, 0]}
                        barSize={20}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card className="border-border/70 bg-surface-panel shadow-sm">
                <CardHeader className="py-3 px-4 border-b border-border/50">
                  <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Répartition par Genre
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-4 flex flex-col items-center justify-center">
                  <div className="h-[180px] w-full relative flex items-center justify-center">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={data.demographics.gender}
                          dataKey="count"
                          nameKey="label"
                          innerRadius={54}
                          outerRadius={74}
                          paddingAngle={3}
                          stroke="none"
                        >
                          {data.demographics.gender.map((_, i) => (
                            <Cell
                              key={i}
                              fill={
                                [
                                  chartPalette.primary,
                                  chartPalette.gold,
                                  chartPalette.cyan,
                                ][i % 3]
                              }
                            />
                          ))}
                        </Pie>
                        <RTooltip contentStyle={DASHBOARD_THEME.tooltipStyle} />
                      </PieChart>
                    </ResponsiveContainer>
                    <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                      <span className="text-2xl font-bold font-mono text-foreground">
                        {genderTotal}
                      </span>
                      <span className="text-[10px] uppercase text-muted-foreground">
                        élèves
                      </span>
                    </div>
                  </div>

                  <div className="flex justify-center gap-6 mt-2 text-xs">
                    {data.demographics.gender.map((g, i) => (
                      <div key={g.label} className="flex items-center gap-2">
                        <span
                          className="h-2.5 w-2.5 rounded-full"
                          style={{
                            backgroundColor: [
                              chartPalette.primary,
                              chartPalette.gold,
                              chartPalette.cyan,
                            ][i % 3],
                          }}
                        />
                        <span className="text-muted-foreground">{g.label}:</span>
                        <strong className="font-mono text-foreground">
                          {g.count}
                        </strong>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="border-border/70 bg-surface-panel shadow-sm">
                <CardHeader className="py-3 px-4 border-b border-border/50">
                  <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Pyramide des Âges
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-4">
                  <div className="h-[200px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={data.demographics.age}>
                        <CartesianGrid
                          strokeDasharray="3 3"
                          stroke={DASHBOARD_THEME.gridStroke}
                          vertical={false}
                        />
                        <XAxis
                          dataKey="label"
                          {...DASHBOARD_THEME.axisTick}
                          axisLine={false}
                          tickLine={false}
                        />
                        <YAxis
                          {...DASHBOARD_THEME.axisTick}
                          axisLine={false}
                          tickLine={false}
                          allowDecimals={false}
                        />
                        <RTooltip contentStyle={DASHBOARD_THEME.tooltipStyle} />
                        <Bar
                          dataKey="count"
                          fill={chartPalette.cyan}
                          radius={[4, 4, 0, 0]}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </PageTabContent>

        {/* 4. DEBT SECTION */}
        <PageTabContent value="debt">
          <div className="space-y-4">
            <Card className="border-border/70 bg-surface-panel shadow-sm">
              <CardHeader className="py-3 px-4 border-b border-border/50">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Structure des Retards par Ancienneté
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <table className="w-full text-xs">
                  <thead className="bg-muted/30 text-muted-foreground text-left">
                    <tr className="border-b border-border/60">
                      <th className="py-2.5 px-4 font-medium">Tranche</th>
                      <th className="py-2.5 px-4 text-right font-medium">
                        Encours
                      </th>
                      <th className="py-2.5 px-4 text-right font-medium">
                        Familles
                      </th>
                      <th className="py-2.5 px-4 text-right font-medium">
                        Sévérité
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border/40">
                    {data.debtAging.map((b) => {
                      const sev = agingSeverity(b.bucket);
                      return (
                        <tr key={b.bucket} className="hover:bg-accent/5">
                          <td className="py-2.5 px-4 font-medium">
                            {AGING_BUCKET_LABELS_FR[b.bucket]}
                          </td>
                          <td className="py-2.5 px-4 text-right font-mono font-bold text-foreground">
                            {formatDzdPlain(b.amount)} DA
                          </td>
                          <td className="py-2.5 px-4 text-right font-mono">
                            {b.debtorCount}
                          </td>
                          <td className="py-2.5 px-4 text-right">
                            <span
                              className={`inline-block px-2 py-0.5 rounded-full border text-[10px] font-bold uppercase ${sev.className}`}
                            >
                              {sev.label}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </CardContent>
            </Card>

            <Card className="border-border/70 bg-surface-panel shadow-sm">
              <CardHeader className="py-3 px-4 border-b border-border/50">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Top Débiteurs Prioritaires (10 Plus Fortes Créances)
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                {data.topDebtors.length === 0 ? (
                  <p className="text-xs text-muted-foreground text-center py-6">
                    Aucune créance enregistrée.
                  </p>
                ) : (
                  <table className="w-full text-xs">
                    <thead className="bg-muted/30 text-muted-foreground text-left">
                      <tr className="border-b border-border/60">
                        <th className="py-2.5 px-4 font-medium">Rang</th>
                        <th className="py-2.5 px-4 font-medium">Famille</th>
                        <th className="py-2.5 px-4 text-right font-medium">
                          Retard
                        </th>
                        <th className="py-2.5 px-4 text-right font-medium">
                          Créance
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border/40">
                      {data.topDebtors.map((d, i) => (
                        <tr key={d.parentId} className="hover:bg-accent/5">
                          <td className="py-2 px-4 font-mono text-muted-foreground">
                            #{i + 1}
                          </td>
                          <td className="py-2 px-4 font-medium text-foreground">
                            {d.parentName}
                          </td>
                          <td className="py-2 px-4 text-right font-mono text-muted-foreground">
                            {d.daysOverdue} j
                          </td>
                          <td className="py-2 px-4 text-right font-mono font-bold text-status-danger">
                            {formatDzdPlain(d.outstandingAmount)} DA
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </CardContent>
            </Card>
          </div>
        </PageTabContent>
      </PageTabs>
    </UnifiedModal>
  );
}

function DepartmentsTab({
  payments,
}: {
  data: DashboardData;
  payments: readonly Payment[];
}) {
  const unitsWithTotals = OPERATIONAL_UNITS.map((u) => {
    const amount = payments
      .filter((p) => u.categories.includes(p.category))
      .reduce((s, p) => s + p.amount, 0);
    return { ...u, amount };
  });

  const claimed = new Set(OPERATIONAL_UNITS.flatMap((u) => u.categories));
  const otherAmount = payments
    .filter((p) => !claimed.has(p.category))
    .reduce((s, p) => s + p.amount, 0);
  const grandTotal =
    unitsWithTotals.reduce((s, u) => s + u.amount, 0) + otherAmount;

  return (
    <Card className="border-border/70 bg-surface-panel shadow-sm">
      <CardHeader className="py-3 px-4 border-b border-border/50">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Ventilation par Pôle Opérationnel
        </CardTitle>
        <CardDescription className="text-xs text-muted-foreground">
          Répartition des encaissements effectifs par activité
        </CardDescription>
      </CardHeader>
      <CardContent className="p-4 space-y-4">
        {grandTotal === 0 ? (
          <p className="text-xs text-muted-foreground text-center py-8">
            Aucun encaissement sur cette période.
          </p>
        ) : (
          <>
            <div className="space-y-3">
              {unitsWithTotals.map((u) => {
                const pct =
                  grandTotal > 0 ? Math.round((u.amount / grandTotal) * 100) : 0;
                return (
                  <div key={u.key} className="space-y-1">
                    <div className="flex justify-between text-xs">
                      <span className="flex items-center gap-1.5 font-medium">
                        <span
                          className="h-2 w-2 rounded-full"
                          style={{ backgroundColor: u.color }}
                        />
                        {u.label}
                      </span>
                      <span className="font-mono font-bold text-foreground">
                        {formatDzd(u.amount)}{" "}
                        <span className="text-muted-foreground font-normal">
                          ({pct}%)
                        </span>
                      </span>
                    </div>
                    <div className="h-1.5 w-full rounded-full bg-muted/60 overflow-hidden">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${pct}%`,
                          backgroundColor: u.color,
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="pt-3 border-t border-border/60 flex items-center justify-between">
              <span className="text-xs font-bold text-foreground">
                Total Encaissé ({payments.length} versements)
              </span>
              <span className="font-mono font-bold text-base text-status-success">
                {formatDzdPlain(grandTotal)} DA
              </span>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
```

---

### Step 9: Redesigning the Academic Year & Date Range Selector (`academic-year-selector.tsx`)

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/academic-year-selector.tsx
// ============================================================================

import { useState, useMemo } from "react";
import { Calendar, ChevronDown, Check, X } from "lucide-react";
import { Button } from "../../shared/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../../shared/ui/dropdown-menu";
import { cn } from "../../shared/ui/cn";

export interface AcademicYearRange {
  academicYear: string;
  range?: { from: string; to: string };
  preset: DateRangePreset;
}

export type DateRangePreset = "ytd" | "month" | "quarter" | "custom";

interface AcademicYearSelectorProps {
  value: AcademicYearRange;
  onChange: (next: AcademicYearRange) => void;
  availableYears: readonly string[];
}

const PRESET_LABELS_FR: Record<DateRangePreset, string> = {
  ytd: "Année Complète",
  month: "Mois Courant",
  quarter: "Trimestre",
  custom: "Plage Libre",
};

export function computeDateRange(
  academicYear: string,
  preset: DateRangePreset,
  now: Date = new Date(),
): { from: string; to: string } {
  const m = /^(\d{4})-(\d{4})$/.exec(academicYear);
  const startYear = m ? parseInt(m[1], 10) : now.getFullYear();
  const yearStart = new Date(startYear, 8, 1);
  const yearEnd = new Date(startYear + 1, 8, 1);

  if (preset === "ytd") {
    return {
      from: yearStart.toISOString().slice(0, 10),
      to: yearEnd.toISOString().slice(0, 10),
    };
  }
  if (preset === "month") {
    const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
    const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 1);
    return {
      from: monthStart.toISOString().slice(0, 10),
      to: monthEnd.toISOString().slice(0, 10),
    };
  }
  if (preset === "quarter") {
    const month = now.getMonth();
    let qStart: Date;
    if (month >= 8 && month <= 10)
      qStart = new Date(now.getFullYear(), 8, 1);
    else if (month === 11 || month <= 1)
      qStart = new Date(
        now.getFullYear() - (month === 11 ? 0 : 1),
        11,
        1,
      );
    else if (month >= 2 && month <= 4)
      qStart = new Date(now.getFullYear(), 2, 1);
    else qStart = new Date(now.getFullYear(), 5, 1);
    const qEnd = new Date(qStart);
    qEnd.setMonth(qEnd.getMonth() + 3);
    return {
      from: qStart.toISOString().slice(0, 10),
      to: qEnd.toISOString().slice(0, 10),
    };
  }

  const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
  const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 1);
  return {
    from: monthStart.toISOString().slice(0, 10),
    to: monthEnd.toISOString().slice(0, 10),
  };
}

export function AcademicYearSelector({
  value,
  onChange,
  availableYears,
}: AcademicYearSelectorProps) {
  const [customFrom, setCustomFrom] = useState("");
  const [customTo, setCustomTo] = useState("");

  const presetLabel = useMemo(
    () => PRESET_LABELS_FR[value.preset],
    [value.preset],
  );
  const showActiveFilter = value.preset !== "ytd";

  function selectYear(year: string) {
    const range = computeDateRange(year, value.preset);
    onChange({ academicYear: year, range, preset: value.preset });
  }

  function selectPreset(preset: DateRangePreset) {
    const range = computeDateRange(value.academicYear, preset);
    onChange({ academicYear: value.academicYear, range, preset });
  }

  function applyCustom() {
    if (!customFrom || !customTo) return;
    onChange({
      academicYear: value.academicYear,
      range: { from: customFrom, to: customTo },
      preset: "custom",
    });
  }

  function reset() {
    const range = computeDateRange(value.academicYear, "ytd");
    onChange({ academicYear: value.academicYear, range, preset: "ytd" });
  }

  return (
    <div className="flex items-center gap-1.5">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="outline"
            size="sm"
            className="h-8 gap-2 border-border/70 bg-surface-panel hover:bg-surface-elevated text-xs font-medium shadow-sm"
          >
            <Calendar className="h-3.5 w-3.5 text-primary" />
            <span className="font-mono font-semibold text-foreground">
              {value.academicYear}
            </span>
            <span className="text-muted-foreground/60">·</span>
            <span className="text-muted-foreground">{presetLabel}</span>
            <ChevronDown className="h-3 w-3 opacity-60 ml-0.5" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-64 p-1.5 shadow-xl">
          <DropdownMenuLabel className="text-[10px] uppercase tracking-wider text-muted-foreground px-2 py-1">
            Année Scolaire
          </DropdownMenuLabel>
          {availableYears.map((year) => (
            <DropdownMenuItem
              key={year}
              onClick={() => selectYear(year)}
              className={cn(
                "flex items-center justify-between text-xs py-1.5 px-2 cursor-pointer rounded-md",
                year === value.academicYear &&
                  "bg-primary/10 text-primary font-semibold",
              )}
            >
              <span className="font-mono">{year}</span>
              {year === value.academicYear && (
                <Check className="h-3.5 w-3.5 text-primary" />
              )}
            </DropdownMenuItem>
          ))}

          <DropdownMenuSeparator className="my-1.5" />
          <DropdownMenuLabel className="text-[10px] uppercase tracking-wider text-muted-foreground px-2 py-1">
            Filtrage Temporel
          </DropdownMenuLabel>
          {(["ytd", "month", "quarter"] as const).map((preset) => (
            <DropdownMenuItem
              key={preset}
              onClick={() => selectPreset(preset)}
              className={cn(
                "flex items-center justify-between text-xs py-1.5 px-2 cursor-pointer rounded-md",
                value.preset === preset &&
                  "bg-primary/10 text-primary font-semibold",
              )}
            >
              <span>{PRESET_LABELS_FR[preset]}</span>
              {value.preset === preset && (
                <Check className="h-3.5 w-3.5 text-primary" />
              )}
            </DropdownMenuItem>
          ))}

          <DropdownMenuSeparator className="my-1.5" />
          <DropdownMenuLabel className="text-[10px] uppercase tracking-wider text-muted-foreground px-2 py-1">
            Plage Personnalisée
          </DropdownMenuLabel>
          <div className="px-2 py-1.5 space-y-2">
            <div className="grid grid-cols-2 gap-1.5">
              <div>
                <label className="text-[9px] uppercase text-muted-foreground block mb-0.5">
                  Du
                </label>
                <input
                  type="date"
                  value={customFrom}
                  onChange={(e) => setCustomFrom(e.target.value)}
                  className="w-full text-xs rounded border border-border bg-background px-1.5 py-1 font-mono"
                />
              </div>
              <div>
                <label className="text-[9px] uppercase text-muted-foreground block mb-0.5">
                  Au
                </label>
                <input
                  type="date"
                  value={customTo}
                  onChange={(e) => setCustomTo(e.target.value)}
                  className="w-full text-xs rounded border border-border bg-background px-1.5 py-1 font-mono"
                />
              </div>
            </div>
            <Button
              size="sm"
              className="w-full h-7 text-xs"
              onClick={applyCustom}
              disabled={!customFrom || !customTo}
            >
              Appliquer la sélection
            </Button>
          </div>
        </DropdownMenuContent>
      </DropdownMenu>

      {showActiveFilter && (
        <Button
          variant="ghost"
          size="sm"
          className="h-8 w-8 p-0 text-muted-foreground hover:text-foreground"
          onClick={reset}
          title="Réinitialiser le filtre"
        >
          <X className="h-3.5 w-3.5" />
        </Button>
      )}
    </div>
  );
}
```

---

### Step 10: Redesigning the Analytics Slicers & Stat Strip (`analytics-slicers.tsx`, `stat-strip.tsx`)

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/analytics-slicers.tsx
// ============================================================================

import { Filter, RotateCcw } from "lucide-react";
import { Button } from "../../../../shared/ui/button";
import {
  PAYMENT_METHOD_LABELS_FR,
  type PaymentMethod,
  type PaymentCategory,
} from "../../../../domain/model/payment";
import { PAYMENT_CATEGORY_LABELS_FR } from "../../../../domain/model/payment";
import {
  hasActiveFilters,
  type AnalyticsFilterState,
} from "./analytics-derivations";
import { formatDzd } from "../../../../core/format/currency";

export interface AnalyticsSlicersProps {
  filters: AnalyticsFilterState;
  onToggleMethod: (method: PaymentMethod) => void;
  onToggleCategory: (category: PaymentCategory) => void;
  onReset: () => void;
  methods: PaymentMethod[];
  categories: PaymentCategory[];
  filteredCount: number;
  filteredTotal: number;
  totalCount: number;
}

function Chip({
  label,
  active,
  onClick,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${
        active
          ? "bg-primary text-primary-foreground border-primary shadow-sm font-semibold"
          : "bg-surface-elevated/40 border-border/70 text-muted-foreground hover:border-primary/40 hover:text-foreground"
      }`}
    >
      {label}
    </button>
  );
}

export function AnalyticsSlicers({
  filters,
  onToggleMethod,
  onToggleCategory,
  onReset,
  methods,
  categories,
  filteredCount,
  filteredTotal,
  totalCount,
}: AnalyticsSlicersProps) {
  const active = hasActiveFilters(filters);

  return (
    <div
      className="rounded-xl border border-border/70 bg-surface-panel p-3.5 space-y-2.5 shadow-sm"
      data-testid="analytics-slicers"
    >
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          <Filter className="h-3.5 w-3.5 text-primary" />
          Filtres Dynamiques (Slicers Interactifs)
        </div>

        <div className="flex items-center gap-3">
          <span
            className="text-xs font-mono text-muted-foreground"
            data-testid="analytics-slicer-badge"
          >
            <strong className="text-foreground">{filteredCount}</strong> /{" "}
            {totalCount} opérations ·{" "}
            <strong className="text-status-success font-bold">
              {formatDzd(filteredTotal, { compact: true })}
            </strong>
          </span>
          {active && (
            <Button
              variant="outline"
              size="sm"
              className="h-7 px-2.5 text-xs border-status-danger/30 text-status-danger hover:bg-status-danger/10"
              onClick={onReset}
              data-testid="analytics-slicer-reset"
            >
              <RotateCcw className="h-3 w-3 mr-1" />
              Réinitialiser
            </Button>
          )}
        </div>
      </div>

      <div className="flex flex-wrap gap-x-6 gap-y-2 pt-1 border-t border-border/40">
        <div
          className="flex items-center gap-1.5 flex-wrap"
          data-testid="analytics-method-chips"
        >
          <span className="text-[10px] uppercase tracking-wide text-muted-foreground font-bold pr-1">
            Mode :
          </span>
          {methods.map((m) => (
            <Chip
              key={m}
              label={PAYMENT_METHOD_LABELS_FR[m]}
              active={filters.methods.has(m)}
              onClick={() => onToggleMethod(m)}
            />
          ))}
        </div>

        {categories.length > 0 && (
          <div
            className="flex items-center gap-1.5 flex-wrap"
            data-testid="analytics-category-chips"
          >
            <span className="text-[10px] uppercase tracking-wide text-muted-foreground font-bold pr-1">
              Pôle :
            </span>
            {categories.map((c) => (
              <Chip
                key={c}
                label={PAYMENT_CATEGORY_LABELS_FR[c]}
                active={filters.categories.has(c)}
                onClick={() => onToggleCategory(c)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
```

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/stat-strip.tsx
// ============================================================================

import {
  Wallet,
  Receipt,
  Scale,
  ArrowUpDown,
  Trophy,
  Activity,
} from "lucide-react";
import { formatDzd } from "../../../../core/format/currency";
import {
  derivePaymentStats,
  type PaymentStats,
} from "./analytics-derivations";
import type { Payment } from "../../../../domain/model/payment";

export interface StatStripProps {
  slice: readonly Payment[];
}

function StatTile({
  icon,
  label,
  value,
  sub,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  sub?: string;
  color: string;
}) {
  return (
    <div className="rounded-xl border border-border/70 bg-surface-panel p-3 flex flex-col justify-between space-y-1 shadow-sm">
      <div className="flex items-center justify-between">
        <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground truncate">
          {label}
        </span>
        <div
          className="h-6 w-6 rounded-md flex items-center justify-center shrink-0"
          style={{
            backgroundColor: `${color}15`,
            color: color,
          }}
        >
          {icon}
        </div>
      </div>
      <div
        className="font-mono text-base font-bold text-foreground tabular-nums truncate"
        title={value}
      >
        {value}
      </div>
      {sub && (
        <div className="text-[10px] text-muted-foreground truncate">
          {sub}
        </div>
      )}
    </div>
  );
}

export function StatStrip({ slice }: StatStripProps) {
  const stats = derivePaymentStats(slice);

  return (
    <div
      className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3"
      data-testid="analytics-stat-strip"
      data-count={stats.count}
      data-total={stats.total}
    >
      <StatTile
        icon={<Wallet className="h-3.5 w-3.5" />}
        label="Total Encaissé"
        value={formatDzd(stats.total, { compact: true })}
        sub={`${stats.count} versements`}
        color="var(--brand-blue, #349bd4)"
      />
      <StatTile
        icon={<Receipt className="h-3.5 w-3.5" />}
        label="Volume Transactions"
        value={String(stats.count)}
        sub="reçus émis"
        color="var(--brand-cyan, #3dd6d0)"
      />
      <StatTile
        icon={<Scale className="h-3.5 w-3.5" />}
        label="Panier Moyen"
        value={stats.count > 0 ? formatDzd(stats.mean, { compact: true }) : "—"}
        sub="moyenne / opération"
        color="var(--status-success, #10b981)"
      />
      <StatTile
        icon={<Activity className="h-3.5 w-3.5" />}
        label="Médiane"
        value={
          stats.count > 0 ? formatDzd(stats.median, { compact: true }) : "—"
        }
        sub="valeur médiane"
        color="var(--brand-violet, #8b5cf6)"
      />
      <StatTile
        icon={<Trophy className="h-3.5 w-3.5" />}
        label="Mois Record"
        value={stats.bestMonth ? stats.bestMonth.label : "—"}
        sub={
          stats.bestMonth
            ? formatDzd(stats.bestMonth.amount, { compact: true })
            : undefined
        }
        color="var(--brand-gold, #eab308)"
      />
      <StatTile
        icon={<ArrowUpDown className="h-3.5 w-3.5" />}
        label="Volatilité (σ)"
        value={
          stats.count > 1 ? formatDzd(stats.stdDev, { compact: true }) : "—"
        }
        sub="dispersion montants"
        color="var(--muted-foreground, #94a3b8)"
      />
    </div>
  );
}
```

---

### Step 11: Redesigning Mix Cards, Aging Composition, and Pareto Visuals (`mix-cards.tsx`, `aging-composition-card.tsx`, `debtors-pareto-card.tsx`)

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/mix-cards.tsx
// ============================================================================

import { useState } from "react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";
import { CreditCard, Layers } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../../shared/ui/card";
import {
  DASHBOARD_THEME,
  chartPalette,
} from "../../../../shared/ui/dashboard-theme";
import { formatDzd, formatDzdPlain } from "../../../../core/format/currency";
import type { Payment } from "../../../../domain/model/payment";
import { deriveMethodMix, deriveCategoryMix } from "./analytics-derivations";

const METHOD_COLORS: Record<string, string> = {
  cash: chartPalette.primary,
  check: chartPalette.gold,
  transfer: chartPalette.cyan,
};

const CATEGORY_COLORS = [
  chartPalette.primary,
  chartPalette.cyan,
  chartPalette.violet,
  chartPalette.gold,
  chartPalette.success,
  chartPalette.info,
  chartPalette.danger,
];

export function MethodMixCard({ slice }: { slice: readonly Payment[] }) {
  const mix = deriveMethodMix(slice);
  const total = mix.reduce((s, m) => s + m.amount, 0);

  return (
    <Card
      className="border-border/70 bg-surface-panel shadow-sm h-full flex flex-col justify-between"
      data-testid="method-mix-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
          <CreditCard className="h-4 w-4 text-primary" />
          Répartition par Mode de Paiement
        </CardTitle>
        <CardDescription className="text-xs text-muted-foreground">
          Volume encaissé selon le canal de règlement
        </CardDescription>
      </CardHeader>

      <CardContent className="p-4 flex-1 flex flex-col justify-center">
        {mix.length === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-10"
            data-testid="method-mix-empty"
          >
            Aucun paiement ne correspond aux filtres actifs.
          </p>
        ) : (
          <div className="space-y-3">
            <div
              className="relative h-[160px] w-full flex items-center justify-center"
              data-testid="method-mix-chart"
            >
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={mix}
                    dataKey="amount"
                    nameKey="label"
                    innerRadius={52}
                    outerRadius={72}
                    paddingAngle={3}
                    stroke="none"
                  >
                    {mix.map((m) => (
                      <Cell
                        key={m.key}
                        fill={METHOD_COLORS[m.key] ?? chartPalette.slate}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={DASHBOARD_THEME.tooltipStyle}
                    formatter={(val: number, name: string) => [
                      `${formatDzdPlain(val)} DZD`,
                      name,
                    ]}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-[10px] uppercase font-bold text-muted-foreground tracking-wider">
                  Total
                </span>
                <span className="font-mono text-sm font-bold text-foreground">
                  {formatDzd(total, { compact: true })}
                </span>
              </div>
            </div>

            <div className="space-y-1.5" data-testid="method-mix-legend">
              {mix.map((m) => (
                <div
                  key={m.key}
                  className="flex items-center justify-between text-xs py-1 px-2 rounded-lg bg-surface-elevated/30 border border-border/30"
                >
                  <span className="flex items-center gap-2">
                    <span
                      className="h-2.5 w-2.5 rounded-full shrink-0"
                      style={{
                        backgroundColor:
                          METHOD_COLORS[m.key] ?? chartPalette.slate,
                      }}
                    />
                    <span className="font-medium text-foreground">{m.label}</span>
                  </span>
                  <span className="font-mono text-muted-foreground">
                    <strong className="text-foreground">{m.percent}%</strong> ·{" "}
                    {formatDzd(m.amount, { compact: true })}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function CategoryMixCard({ slice }: { slice: readonly Payment[] }) {
  const [metric, setMetric] = useState<"amount" | "count">("amount");
  const mix = deriveCategoryMix(slice);
  const maxMetric = Math.max(
    ...mix.map((m) => (metric === "amount" ? m.amount : m.count)),
    0,
  );

  return (
    <Card
      className="border-border/70 bg-surface-panel shadow-sm h-full flex flex-col justify-between"
      data-testid="category-mix-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between gap-2">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Layers className="h-4 w-4 text-brand-cyan" />
            Répartition par Pôle Tarifaire
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Ventilation des recettes par service
          </CardDescription>
        </div>

        <div
          className="flex rounded-md border border-border bg-surface-elevated/40 p-0.5 text-xs"
          data-testid="category-metric-toggle"
        >
          <button
            type="button"
            onClick={() => setMetric("amount")}
            aria-pressed={metric === "amount"}
            className={`px-2.5 py-1 rounded transition-colors ${
              metric === "amount"
                ? "bg-primary text-primary-foreground font-semibold"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Montant
          </button>
          <button
            type="button"
            onClick={() => setMetric("count")}
            aria-pressed={metric === "count"}
            className={`px-2.5 py-1 rounded transition-colors ${
              metric === "count"
                ? "bg-primary text-primary-foreground font-semibold"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Nb Opérations
          </button>
        </div>
      </CardHeader>

      <CardContent className="p-4 flex-1">
        {mix.length === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-10"
            data-testid="category-mix-empty"
          >
            Aucun paiement ne correspond aux filtres actifs.
          </p>
        ) : (
          <div className="h-[210px] w-full" data-testid="category-mix-chart">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={mix}
                layout="vertical"
                margin={{ top: 0, right: 12, bottom: 0, left: 0 }}
              >
                <XAxis
                  type="number"
                  hide
                  domain={[0, maxMetric === 0 ? 1 : maxMetric]}
                />
                <YAxis
                  type="category"
                  dataKey="label"
                  width={130}
                  {...DASHBOARD_THEME.axisTick}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={DASHBOARD_THEME.tooltipStyle}
                  formatter={(val: number) => [
                    metric === "amount"
                      ? `${formatDzdPlain(val)} DZD`
                      : `${val} opération(s)`,
                    "Volume",
                  ]}
                />
                <Bar dataKey={metric} radius={[0, 4, 4, 0]} barSize={16}>
                  {mix.map((m, i) => (
                    <Cell
                      key={m.key}
                      fill={CATEGORY_COLORS[i % CATEGORY_COLORS.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/aging-composition-card.tsx
// ============================================================================

import { useMemo, useState } from "react";
import { Hourglass } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../../shared/ui/card";
import { AGING_COLORS } from "../../tabs/types";
import { formatDzd, formatDzdPlain } from "../../../../core/format/currency";
import type { DebtByAgingBucket } from "../../../../domain/model/operations";
import { deriveAgingComposition } from "./analytics-derivations";

export function AgingCompositionCard({
  debtAging,
}: {
  debtAging: DebtByAgingBucket[];
}) {
  const segments = useMemo(
    () => deriveAgingComposition(debtAging),
    [debtAging],
  );
  const [hover, setHover] = useState<string | null>(null);
  const total = segments.reduce((s, x) => s + x.amount, 0);
  const totalFamilies = segments.reduce((s, x) => s + x.debtorCount, 0);

  return (
    <Card
      className="border-border/70 bg-surface-panel shadow-sm h-full flex flex-col justify-between"
      data-testid="aging-composition-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between flex-wrap gap-2">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Hourglass className="h-4 w-4 text-primary" />
            Structure d'Ancienneté de l'Encours
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Répartition proportionnelle de la dette globale
          </CardDescription>
        </div>

        {segments.length > 0 && (
          <span className="text-xs font-mono font-bold text-status-danger">
            {formatDzd(total, { compact: true })} · {totalFamilies} familles
          </span>
        )}
      </CardHeader>

      <CardContent className="p-4 space-y-4 flex-1 flex flex-col justify-center">
        {segments.length === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-10"
            data-testid="aging-empty"
          >
            Aucune créance ouverte sur la période active.
          </p>
        ) : (
          <>
            {/* 100% Stacked Bar */}
            <div
              className="flex h-7 w-full rounded-xl overflow-hidden border border-border/60 shadow-inner"
              data-testid="aging-stacked-bar"
            >
              {segments.map((seg) => (
                <div
                  key={seg.bucket}
                  role="progressbar"
                  aria-label={`${seg.label} : ${seg.share}%`}
                  onMouseEnter={() => setHover(seg.bucket)}
                  onMouseLeave={() => setHover(null)}
                  className="h-full flex items-center justify-center transition-all cursor-pointer"
                  style={{
                    width: `${seg.share}%`,
                    backgroundColor: AGING_COLORS[seg.bucket],
                    opacity:
                      hover === null || hover === seg.bucket ? 1 : 0.45,
                  }}
                >
                  {seg.share >= 10 && (
                    <span className="text-[11px] font-mono font-bold text-white drop-shadow">
                      {seg.share}%
                    </span>
                  )}
                </div>
              ))}
            </div>

            {/* Table Breakdown */}
            <div className="overflow-x-auto">
              <table
                className="w-full text-xs"
                data-testid="aging-table"
              >
                <thead>
                  <tr className="text-muted-foreground border-b border-border/60 text-left">
                    <th className="py-2 px-2 font-medium">Tranche de Retard</th>
                    <th className="py-2 px-2 text-right font-medium">Encours</th>
                    <th className="py-2 px-2 text-right font-medium">
                      Familles
                    </th>
                    <th className="py-2 px-2 text-right font-medium">Part</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/40">
                  {segments.map((seg) => (
                    <tr
                      key={seg.bucket}
                      className={`hover:bg-accent/5 transition-colors ${
                        hover === seg.bucket ? "bg-primary/10" : ""
                      }`}
                      onMouseEnter={() => setHover(seg.bucket)}
                      onMouseLeave={() => setHover(null)}
                    >
                      <td className="py-2 px-2 flex items-center gap-2 font-medium">
                        <span
                          className="h-2 w-2 rounded-full shrink-0"
                          style={{ backgroundColor: AGING_COLORS[seg.bucket] }}
                        />
                        {seg.label}
                      </td>
                      <td className="text-right font-mono font-bold text-foreground py-2 px-2">
                        {formatDzd(seg.amount, { compact: true })}
                      </td>
                      <td className="text-right font-mono py-2 px-2">
                        {seg.debtorCount}
                      </td>
                      <td className="text-right font-mono py-2 px-2 text-muted-foreground">
                        {seg.share}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
```

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/debtors-pareto-card.tsx
// ============================================================================

import { useMemo } from "react";
import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { Users } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../../shared/ui/card";
import {
  DASHBOARD_THEME,
  chartPalette,
} from "../../../../shared/ui/dashboard-theme";
import { formatDzd, formatDzdPlain } from "../../../../core/format/currency";
import type { DebtSummary } from "../../../../domain/model/payment";
import { derivePareto } from "./analytics-derivations";

function shortName(full: string): string {
  const trimmed = full.replace(/^Famille\s+/i, "").trim();
  const parts = trimmed.split(/\s+/);
  if (parts.length === 0) return trimmed;
  const initial = parts[0].charAt(0).toUpperCase();
  const lastName = parts[parts.length - 1];
  return `${initial}. ${lastName}`;
}

export function DebtorsParetoCard({
  topDebtors,
}: {
  topDebtors: DebtSummary[];
}) {
  const data = useMemo(() => derivePareto(topDebtors), [topDebtors]);
  const displayedTotal = data.reduce((s, d) => s + d.amount, 0);
  const paretoCut = data.findIndex((d) => d.cumPercent >= 80) + 1;
  const chartData = data.map((d) => ({ ...d, short: shortName(d.name) }));

  return (
    <Card
      className="border-border/70 bg-surface-panel shadow-sm h-full flex flex-col justify-between"
      data-testid="debtors-pareto-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between flex-wrap gap-2">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Users className="h-4 w-4 text-status-danger" />
            Distribution Pareto des Créances (Règle des 80/20)
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Concentration cumulée des impayés par tuteur
          </CardDescription>
        </div>

        {paretoCut > 0 && (
          <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-status-warning/15 text-status-warning border border-status-warning/30">
            {paretoCut} foyer(s) = 80% de l'encours
          </span>
        )}
      </CardHeader>

      <CardContent className="p-4 flex-1">
        {data.length === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-10"
            data-testid="pareto-empty"
          >
            Aucun débiteur identifié sur la période active.
          </p>
        ) : (
          <div className="h-[230px] w-full" data-testid="pareto-chart">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart
                data={chartData}
                margin={{ top: 10, right: 0, bottom: 0, left: -10 }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke={DASHBOARD_THEME.gridStroke}
                  vertical={false}
                />
                <XAxis
                  dataKey="short"
                  {...DASHBOARD_THEME.axisTick}
                  axisLine={false}
                  tickLine={false}
                  interval={0}
                  angle={-25}
                  textAnchor="end"
                  height={45}
                />
                <YAxis
                  yAxisId="amount"
                  {...DASHBOARD_THEME.axisTick}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v: number) =>
                    `${Math.round(v / 1000)}k`
                  }
                />
                <YAxis
                  yAxisId="percent"
                  orientation="right"
                  domain={[0, 100]}
                  {...DASHBOARD_THEME.axisTick}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v: number) => `${v}%`}
                />
                <Tooltip
                  contentStyle={DASHBOARD_THEME.tooltipStyle}
                  formatter={(
                    val: number,
                    name: string,
                    entry: { payload?: { name?: string } },
                  ) => {
                    if (name === "amount") {
                      return [
                        `${formatDzdPlain(val)} DZD`,
                        entry?.payload?.name ?? "Dette",
                      ];
                    }
                    return [`${val}%`, "Part cumulée"];
                  }}
                />
                <Bar
                  yAxisId="amount"
                  dataKey="amount"
                  fill={chartPalette.danger}
                  radius={[4, 4, 0, 0]}
                  barSize={20}
                />
                <Line
                  yAxisId="percent"
                  dataKey="cumPercent"
                  type="monotone"
                  stroke={chartPalette.gold}
                  strokeWidth={2}
                  dot={{ r: 2.5, fill: chartPalette.gold }}
                />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/yoy-comparison-card.tsx
// ============================================================================

import { ArrowRight, Calendar } from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../../shared/ui/card";
import {
  DASHBOARD_THEME,
  chartPalette,
} from "../../../../shared/ui/dashboard-theme";
import { formatDzd, formatDzdPlain } from "../../../../core/format/currency";
import type { RevenuePoint } from "../../../../domain/model/operations";
import { deriveYearOverYear } from "./analytics-derivations";

export function YoYComparisonCard({
  currentYear,
  previousYear,
  revenue,
  prevRevenue,
}: {
  currentYear: string;
  previousYear: string | null;
  revenue: readonly RevenuePoint[];
  prevRevenue: readonly RevenuePoint[];
}) {
  const summary = deriveYearOverYear(revenue, prevRevenue);
  const hasPrevious = prevRevenue.length > 0;

  return (
    <Card
      className="border-border/70 bg-surface-panel shadow-sm h-full flex flex-col justify-between"
      data-testid="yoy-comparison-card"
    >
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between flex-wrap gap-2">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Calendar className="h-4 w-4 text-primary" />
            Évolution des Recettes en Glissement Annuel (N vs N−1)
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Comparaison directe mois par mois à périmètre constant
          </CardDescription>
        </div>

        {hasPrevious && summary.deltaPercent !== null && (
          <span
            className={`text-xs font-mono font-bold px-2 py-0.5 rounded-full border ${
              summary.deltaPercent >= 0
                ? "bg-status-success/15 text-status-success border-status-success/30"
                : "bg-status-danger/15 text-status-danger border-status-danger/30"
            }`}
          >
            {summary.deltaPercent >= 0 ? "▲ +" : "▼ "}
            {summary.deltaPercent}% global
          </span>
        )}
      </CardHeader>

      <CardContent className="p-4 flex-1">
        {!hasPrevious ? (
          <p
            className="text-xs text-muted-foreground text-center py-10"
            data-testid="yoy-unavailable"
          >
            Données de l'année précédente non disponibles pour {currentYear}.
          </p>
        ) : revenue.length === 0 ? (
          <p
            className="text-xs text-muted-foreground text-center py-10"
            data-testid="yoy-empty"
          >
            Aucun encaissement sur cette période.
          </p>
        ) : (
          <div className="h-[220px] w-full" data-testid="yoy-chart">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={summary.points}
                margin={{ top: 10, right: 8, bottom: 0, left: -14 }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke={DASHBOARD_THEME.gridStroke}
                  vertical={false}
                />
                <XAxis
                  dataKey="label"
                  {...DASHBOARD_THEME.axisTick}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  {...DASHBOARD_THEME.axisTick}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v: number) =>
                    `${Math.round(v / 1000)}k`
                  }
                />
                <Tooltip
                  contentStyle={DASHBOARD_THEME.tooltipStyle}
                  formatter={(val: number, name: string) => [
                    `${formatDzdPlain(val)} DZD`,
                    name,
                  ]}
                />
                <Bar
                  dataKey="previous"
                  name={`N−1 (${previousYear})`}
                  fill={chartPalette.slate}
                  radius={[3, 3, 0, 0]}
                  barSize={14}
                />
                <Bar
                  dataKey="current"
                  name={`N (${currentYear})`}
                  fill={chartPalette.primary}
                  radius={[3, 3, 0, 0]}
                  barSize={14}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

---

### Step 12: Redesigning the Risk Matrix & Operational Query Console (`cross-risk-card.tsx`, `operational-query-console.tsx`, `pivot-matrix-card.tsx`)

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/cross-risk-card.tsx
// ============================================================================

import { AlertTriangle, TrendingDown, Clock, Wallet, Bot } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../../shared/ui/card";
import { Button } from "../../../../shared/ui/button";
import { useAICopilot } from "../../../../app/providers/ai-copilot-provider";
import type { StudentRiskProfile } from "./operational-query-engine";

interface Props {
  profiles: StudentRiskProfile[];
  onSelectCategory?: (category: string) => void;
}

export function CrossRiskCard({ profiles, onSelectCategory }: Props) {
  const { askAgent, setIsOpen: openCopilot } = useAICopilot();

  const counts = {
    triple: profiles.filter((p) => p.riskCategory === "triple_critical").length,
    academic: profiles.filter((p) => p.riskCategory === "academic_alert").length,
    attendance: profiles.filter(
      (p) => p.riskCategory === "attendance_alert",
    ).length,
    financial: profiles.filter(
      (p) => p.riskCategory === "financial_tension",
    ).length,
  };

  const handleLaunchEmergencyInvestigation = () => {
    const prompt =
      `Audit d'urgence sur les vulnérabilités de l'établissement :\n` +
      `- ${counts.triple} élève(s) en Triple Risque critique\n` +
      `- ${counts.academic} élève(s) en difficulté académique (GPA < 10)\n` +
      `- ${counts.attendance} élève(s) en alerte assiduité\n` +
      `- ${counts.financial} famille(s) en tension financière élevée\n\n` +
      `Construis un plan de remédiation opérationnel avec priorisation et actions immédiates.`;

    openCopilot(true);
    void askAgent(prompt);
  };

  return (
    <Card className="border-border/70 bg-surface-panel shadow-sm h-full flex flex-col justify-between">
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between flex-wrap gap-2">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 text-status-warning" />
            Triage des Vulnérabilités Croisées
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Distribution selon les 4 axes de vigilance opérationnelle
          </CardDescription>
        </div>

        <Button
          size="sm"
          variant="outline"
          onClick={handleLaunchEmergencyInvestigation}
          className="h-7 text-xs border-primary/40 text-primary gap-1.5"
        >
          <Bot className="h-3.5 w-3.5" />
          Audit IA
        </Button>
      </CardHeader>

      <CardContent className="p-4 space-y-3 flex-1 flex flex-col justify-between">
        <div className="grid grid-cols-2 gap-3">
          {/* 1. Triple Risque */}
          <div
            onClick={() => onSelectCategory?.("triple_critical")}
            className="p-3.5 rounded-xl border border-status-danger/40 bg-status-danger/10 cursor-pointer hover:bg-status-danger/15 transition-all space-y-1"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-status-danger">
                Triple Risque
              </span>
              <AlertTriangle className="h-4 w-4 text-status-danger" />
            </div>
            <div className="text-2xl font-mono font-bold text-status-danger">
              {counts.triple}
            </div>
            <p className="text-[10px] text-muted-foreground">
              Notes + Absences + Dette
            </p>
          </div>

          {/* 2. Échec scolaire */}
          <div
            onClick={() => onSelectCategory?.("academic_alert")}
            className="p-3.5 rounded-xl border border-status-warning/40 bg-status-warning/10 cursor-pointer hover:bg-status-warning/15 transition-all space-y-1"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-status-warning">
                Moyenne &lt; 10
              </span>
              <TrendingDown className="h-4 w-4 text-status-warning" />
            </div>
            <div className="text-2xl font-mono font-bold text-status-warning">
              {counts.academic}
            </div>
            <p className="text-[10px] text-muted-foreground">
              Décrochage pédagogique
            </p>
          </div>

          {/* 3. Assiduité */}
          <div
            onClick={() => onSelectCategory?.("attendance_alert")}
            className="p-3.5 rounded-xl border border-border/70 bg-surface-elevated/40 cursor-pointer hover:bg-surface-elevated/70 transition-all space-y-1"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-foreground">
                Assiduité
              </span>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </div>
            <div className="text-2xl font-mono font-bold text-foreground">
              {counts.attendance}
            </div>
            <p className="text-[10px] text-muted-foreground">
              ≥ 3 absences non justifiées
            </p>
          </div>

          {/* 4. Retards de paiement */}
          <div
            onClick={() => onSelectCategory?.("financial_tension")}
            className="p-3.5 rounded-xl border border-border/70 bg-surface-elevated/40 cursor-pointer hover:bg-surface-elevated/70 transition-all space-y-1"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-foreground">
                Tension Dette
              </span>
              <Wallet className="h-4 w-4 text-muted-foreground" />
            </div>
            <div className="text-2xl font-mono font-bold text-foreground">
              {counts.financial}
            </div>
            <p className="text-[10px] text-muted-foreground">
              Solde dû &gt; 25 000 DA
            </p>
          </div>
        </div>

        <p className="text-[11px] text-muted-foreground text-center">
          Cliquez sur un quadrant pour filtrer la console d'investigation.
        </p>
      </CardContent>
    </Card>
  );
}
```

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/pivot-matrix-card.tsx
// ============================================================================

import { useState, useMemo } from "react";
import { Layers, ArrowUpDown } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../../shared/ui/card";
import { formatDzd, formatDzdPlain } from "../../../../core/format/currency";
import type { AcademicClass } from "../../../../domain/model/academic";
import {
  computeMultiDimensionalPivot,
  type StudentRiskProfile,
  type PivotDimension,
} from "./operational-query-engine";

interface Props {
  profiles: StudentRiskProfile[];
  classes: readonly AcademicClass[];
}

export function PivotMatrixCard({ profiles, classes }: Props) {
  const [dimension, setDimension] = useState<PivotDimension>("cycle");
  const [sortKey, setSortKey] = useState<
    "studentCount" | "totalDebt" | "averageGpa"
  >("totalDebt");
  const [sortAsc, setSortAsc] = useState(false);

  const pivotRows = useMemo(() => {
    const raw = computeMultiDimensionalPivot({
      profiles,
      classes,
      dimension,
    });
    return raw.sort((a, b) => {
      const valA = a[sortKey] ?? -1;
      const valB = b[sortKey] ?? -1;
      if (valA === valB) return 0;
      return sortAsc ? (valA > valB ? 1 : -1) : valA < valB ? 1 : -1;
    });
  }, [profiles, classes, dimension, sortKey, sortAsc]);

  const grandTotals = useMemo(() => {
    const totalStudents = pivotRows.reduce(
      (s, r) => s + r.studentCount,
      0,
    );
    const totalDebt = pivotRows.reduce((s, r) => s + r.totalDebt, 0);
    const criticalTotal = pivotRows.reduce(
      (s, r) => s + r.criticalStudentsCount,
      0,
    );
    return { totalStudents, totalDebt, criticalTotal };
  }, [pivotRows]);

  return (
    <Card className="border-border/70 bg-surface-panel shadow-sm h-full flex flex-col justify-between">
      <CardHeader className="py-3 px-4 border-b border-border/50 flex flex-row items-center justify-between flex-wrap gap-2">
        <div>
          <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Layers className="h-4 w-4 text-primary" />
            Matrice Croisée Multi-Dimensionnelle
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground">
            Performances académiques, assiduité et créances par segment
          </CardDescription>
        </div>

        <div className="flex rounded-md border border-border bg-surface-elevated/40 p-0.5 text-xs">
          <button
            type="button"
            onClick={() => setDimension("cycle")}
            className={`px-2.5 py-1 rounded transition-colors ${
              dimension === "cycle"
                ? "bg-primary text-primary-foreground font-semibold"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Cycles
          </button>
          <button
            type="button"
            onClick={() => setDimension("grade")}
            className={`px-2.5 py-1 rounded transition-colors ${
              dimension === "grade"
                ? "bg-primary text-primary-foreground font-semibold"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Paliers
          </button>
          <button
            type="button"
            onClick={() => setDimension("class")}
            className={`px-2.5 py-1 rounded transition-colors ${
              dimension === "class"
                ? "bg-primary text-primary-foreground font-semibold"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Classes
          </button>
        </div>
      </CardHeader>

      <CardContent className="p-0 flex-1 overflow-x-auto">
        <table className="w-full text-xs">
          <thead className="bg-muted/30 text-muted-foreground text-left">
            <tr className="border-b border-border/60">
              <th className="py-2.5 px-3 font-medium">Segment</th>
              <th
                className="py-2.5 px-3 text-right font-medium cursor-pointer"
                onClick={() => {
                  setSortKey("studentCount");
                  setSortAsc(!sortAsc);
                }}
              >
                Effectif <ArrowUpDown className="h-2.5 w-2.5 inline ml-0.5" />
              </th>
              <th
                className="py-2.5 px-3 text-right font-medium cursor-pointer"
                onClick={() => {
                  setSortKey("totalDebt");
                  setSortAsc(!sortAsc);
                }}
              >
                Créances <ArrowUpDown className="h-2.5 w-2.5 inline ml-0.5" />
              </th>
              <th
                className="py-2.5 px-3 text-center font-medium cursor-pointer"
                onClick={() => {
                  setSortKey("averageGpa");
                  setSortAsc(!sortAsc);
                }}
              >
                Moyenne <ArrowUpDown className="h-2.5 w-2.5 inline ml-0.5" />
              </th>
              <th className="py-2.5 px-3 text-center font-medium">
                Assiduité
              </th>
              <th className="py-2.5 px-3 text-right font-medium">
                Alertes
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/40">
            {pivotRows.map((r) => (
              <tr key={r.dimensionKey} className="hover:bg-accent/5">
                <td className="py-2.5 px-3 font-medium text-foreground">
                  {r.dimensionLabel}
                </td>
                <td className="py-2.5 px-3 text-right font-mono font-bold">
                  {r.studentCount}
                </td>
                <td className="py-2.5 px-3 text-right font-mono">
                  {r.totalDebt > 0 ? (
                    <span className="text-status-danger font-bold">
                      {formatDzdPlain(r.totalDebt)} DA
                    </span>
                  ) : (
                    <span className="text-status-success font-medium">0 DA</span>
                  )}
                </td>
                <td className="py-2.5 px-3 text-center font-mono">
                  {r.averageGpa !== null ? (
                    <span
                      className={`font-semibold ${
                        r.averageGpa >= 10
                          ? "text-status-success"
                          : "text-status-danger"
                      }`}
                    >
                      {r.averageGpa.toFixed(2)}/20
                    </span>
                  ) : (
                    <span className="text-muted-foreground">—</span>
                  )}
                </td>
                <td className="py-2.5 px-3 text-center font-mono">
                  {(r.attendanceRate * 100).toFixed(0)}%
                </td>
                <td className="py-2.5 px-3 text-right font-mono">
                  {r.criticalStudentsCount > 0 ? (
                    <span className="px-1.5 py-0.5 rounded-full text-[10px] bg-status-danger/15 text-status-danger font-bold">
                      {r.criticalStudentsCount}
                    </span>
                  ) : (
                    <span className="text-muted-foreground">0</span>
                  )}
                </td>
              </tr>
            ))}
            <tr className="font-bold border-t-2 border-border/80 bg-surface-elevated/30">
              <td className="py-2.5 px-3">Total Général</td>
              <td className="py-2.5 px-3 text-right font-mono">
                {grandTotals.totalStudents}
              </td>
              <td className="py-2.5 px-3 text-right font-mono text-status-danger">
                {formatDzd(grandTotals.totalDebt, { compact: true })}
              </td>
              <td className="py-2.5 px-3 text-center font-mono">—</td>
              <td className="py-2.5 px-3 text-center font-mono">—</td>
              <td className="py-2.5 px-3 text-right font-mono text-status-danger">
                {grandTotals.criticalTotal}
              </td>
            </tr>
          </tbody>
        </table>
      </CardContent>
    </Card>
  );
}
```

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/components/analytics/operational-query-console.tsx
// ============================================================================

import { useState, useMemo } from "react";
import {
  Search,
  MessageCircle,
  ExternalLink,
  Bot,
  Filter,
  CheckCircle2,
  ArrowUpDown,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../../../../shared/ui/card";
import { Button } from "../../../../shared/ui/button";
import { Input } from "../../../../shared/ui/input";
import { Badge } from "../../../../shared/ui/badge";
import { formatDzdPlain } from "../../../../core/format/currency";
import { useAICopilot } from "../../../../app/providers/ai-copilot-provider";
import {
  OPERATIONAL_PRESETS,
  type StudentRiskProfile,
} from "./operational-query-engine";

interface Props {
  profiles: StudentRiskProfile[];
  onOpenStudent?: (studentId: string) => void;
  onOpenParent?: (parentId: string) => void;
}

export function OperationalQueryConsole({
  profiles,
  onOpenStudent,
}: Props) {
  const { askAgent, setIsOpen: openCopilot } = useAICopilot();

  const [search, setSearch] = useState("");
  const [activePreset, setActivePreset] = useState<string | null>(
    "triple_critical",
  );
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [sortField, setSortField] = useState<
    "riskScore" | "debtAmount" | "gpa"
  >("riskScore");
  const [sortAsc, setSortAsc] = useState(false);

  const filteredProfiles = useMemo(() => {
    return profiles
      .filter((p) => {
        if (activePreset) {
          const preset = OPERATIONAL_PRESETS.find(
            (pr) => pr.id === activePreset,
          );
          if (preset) {
            if (
              preset.filterCategory &&
              p.riskCategory !== preset.filterCategory
            )
              return false;
            if (preset.customFilter && !preset.customFilter(p)) return false;
          }
        }

        if (selectedCategory !== "all" && p.riskCategory !== selectedCategory) {
          return false;
        }

        if (search.trim()) {
          const q = search.toLowerCase();
          return (
            p.studentName.toLowerCase().includes(q) ||
            p.studentCode.toLowerCase().includes(q) ||
            p.parentName.toLowerCase().includes(q) ||
            p.className.toLowerCase().includes(q)
          );
        }

        return true;
      })
      .sort((a, b) => {
        const valA = a[sortField] ?? -1;
        const valB = b[sortField] ?? -1;
        if (valA === valB) return 0;
        return sortAsc ? (valA > valB ? 1 : -1) : valA < valB ? 1 : -1;
      });
  }, [profiles, activePreset, selectedCategory, search, sortField, sortAsc]);

  const queryStats = useMemo(() => {
    const count = filteredProfiles.length;
    const totalDebt = filteredProfiles.reduce(
      (s, p) => s + p.debtAmount,
      0,
    );
    const gpas = filteredProfiles
      .map((p) => p.gpa)
      .filter((g): g is number => g !== null);
    const avgGpa =
      gpas.length > 0
        ? gpas.reduce((s, g) => s + g, 0) / gpas.length
        : null;
    return { count, totalDebt, avgGpa };
  }, [filteredProfiles]);

  const handleAskAIAboutCohort = () => {
    if (filteredProfiles.length === 0) return;
    const topSample = filteredProfiles
      .slice(0, 5)
      .map(
        (p) =>
          `- ${p.studentName} (${p.className}) : GPA ${p.gpa ?? "N/A"}/20, ${p.unexcusedAbsences} abs., Dette: ${p.debtAmount} DA`,
      )
      .join("\n");

    const prompt =
      `Analyse de la cohorte sous le filtre « ${activePreset ?? selectedCategory} » (${filteredProfiles.length} élèves identifiés, dette cumulée: ${queryStats.totalDebt.toLocaleString("fr-FR")} DA) :\n${topSample}\n\n` +
      `Donne un diagnostic synthétique et 3 actions prioritaires.`;

    openCopilot(true);
    void askAgent(prompt);
  };

  const handleAskAIAboutStudent = (profile: StudentRiskProfile) => {
    const prompt =
      `Diagnostic personnalisé pour l'élève ${profile.studentName} (${profile.className}) :\n` +
      `- Moyenne : ${profile.gpa ?? "N/A"}/20\n` +
      `- Assiduité : ${(profile.attendanceRate * 100).toFixed(0)}% (${profile.unexcusedAbsences} absences)\n` +
      `- Créance : ${profile.debtAmount.toLocaleString("fr-FR")} DA (${profile.daysOverdue} j retard)\n` +
      `Propose une recommandation concrète pour la direction.`;

    openCopilot(true);
    void askAgent(prompt);
  };

  return (
    <Card className="border-border/70 bg-surface-panel shadow-sm">
      <CardHeader className="py-3.5 px-4 border-b border-border/50 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <CardTitle className="text-sm font-semibold flex items-center gap-2">
              <Search className="h-4 w-4 text-primary" />
              Console d'Investigation Opérationnelle
            </CardTitle>
            <CardDescription className="text-xs text-muted-foreground">
              Interrogation temps réel : profil académique, présence et statut financier
            </CardDescription>
          </div>

          {filteredProfiles.length > 0 && (
            <Button
              size="sm"
              variant="outline"
              onClick={handleAskAIAboutCohort}
              className="h-8 gap-1.5 border-primary/40 bg-primary/5 text-primary text-xs"
            >
              <Bot className="h-3.5 w-3.5" />
              Interroger l'IA sur cette sélection ({filteredProfiles.length})
            </Button>
          )}
        </div>

        {/* Quick Presets */}
        <div className="flex items-center gap-1.5 flex-wrap pt-1">
          <span className="text-[11px] font-bold uppercase text-muted-foreground mr-1 flex items-center gap-1">
            <Filter className="h-3 w-3" /> Requêtes rapides :
          </span>
          {OPERATIONAL_PRESETS.map((preset) => {
            const isActive = activePreset === preset.id;
            return (
              <button
                key={preset.id}
                type="button"
                onClick={() => {
                  if (isActive) setActivePreset(null);
                  else {
                    setActivePreset(preset.id);
                    setSelectedCategory("all");
                  }
                }}
                className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${
                  isActive
                    ? "bg-primary text-primary-foreground border-primary shadow-sm font-semibold"
                    : "bg-surface-elevated/40 text-muted-foreground border-border/70 hover:border-primary/40 hover:text-foreground"
                }`}
              >
                {preset.title}
              </button>
            );
          })}
        </div>
      </CardHeader>

      <CardContent className="p-4 space-y-3.5">
        {/* Search & Sort Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative flex-1 min-w-[240px]">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Rechercher par élève, parent, code ou classe…"
              className="h-8 pl-8 text-xs bg-surface-elevated/40"
            />
          </div>

          <div className="flex items-center gap-1.5 text-xs">
            <span className="text-muted-foreground">Trier :</span>
            <Button
              variant={sortField === "riskScore" ? "default" : "outline"}
              size="sm"
              className="h-8 text-xs"
              onClick={() => {
                if (sortField === "riskScore") setSortAsc(!sortAsc);
                else {
                  setSortField("riskScore");
                  setSortAsc(false);
                }
              }}
            >
              Niveau de Risque
              <ArrowUpDown className="h-3 w-3 ml-1" />
            </Button>
            <Button
              variant={sortField === "debtAmount" ? "default" : "outline"}
              size="sm"
              className="h-8 text-xs"
              onClick={() => {
                if (sortField === "debtAmount") setSortAsc(!sortAsc);
                else {
                  setSortField("debtAmount");
                  setSortAsc(false);
                }
              }}
            >
              Créance
              <ArrowUpDown className="h-3 w-3 ml-1" />
            </Button>
            <Button
              variant={sortField === "gpa" ? "default" : "outline"}
              size="sm"
              className="h-8 text-xs"
              onClick={() => {
                if (sortField === "gpa") setSortAsc(!sortAsc);
                else {
                  setSortField("gpa");
                  setSortAsc(true);
                }
              }}
            >
              Moyenne
              <ArrowUpDown className="h-3 w-3 ml-1" />
            </Button>
          </div>
        </div>

        {/* Live Counter Bar */}
        <div className="flex items-center justify-between text-xs px-3 py-2 rounded-lg bg-surface-elevated/40 border border-border/50 text-muted-foreground">
          <span>
            Dossiers filtrés :{" "}
            <strong className="text-foreground font-mono">
              {queryStats.count}
            </strong>
          </span>
          <div className="flex items-center gap-4">
            {queryStats.totalDebt > 0 && (
              <span>
                Créances cumulées :{" "}
                <strong className="text-status-danger font-mono font-bold">
                  {formatDzdPlain(queryStats.totalDebt)} DA
                </strong>
              </span>
            )}
            {queryStats.avgGpa !== null && (
              <span>
                Moyenne cohorte :{" "}
                <strong className="text-foreground font-mono font-bold">
                  {queryStats.avgGpa.toFixed(2)}/20
                </strong>
              </span>
            )}
          </div>
        </div>

        {/* Results Table */}
        <div className="rounded-xl border border-border/70 overflow-hidden">
          {filteredProfiles.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground text-xs space-y-1">
              <CheckCircle2 className="h-8 w-8 mx-auto text-status-success/60 mb-2" />
              <p className="font-semibold text-foreground">
                Aucun dossier ne correspond à ces critères.
              </p>
              <p>Tous les profils vérifiés sont réguliers.</p>
            </div>
          ) : (
            <div className="max-h-[380px] overflow-y-auto">
              <table className="w-full text-xs">
                <thead className="bg-muted/30 text-muted-foreground sticky top-0 bg-surface-panel z-10 text-left">
                  <tr className="border-b border-border/60">
                    <th className="py-2.5 px-3 font-medium">Élève & Classe</th>
                    <th className="py-2.5 px-3 font-medium">Parent & Contact</th>
                    <th className="py-2.5 px-2 text-center font-medium">
                      Moyenne
                    </th>
                    <th className="py-2.5 px-2 text-center font-medium">
                      Présence
                    </th>
                    <th className="py-2.5 px-3 text-right font-medium">
                      Créance
                    </th>
                    <th className="py-2.5 px-3 font-medium">
                      Facteur d'Alerte
                    </th>
                    <th className="py-2.5 px-3 text-right font-medium">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/40">
                  {filteredProfiles.map((p) => (
                    <tr
                      key={p.studentId}
                      className="hover:bg-accent/5 transition-colors"
                    >
                      <td className="py-2 px-3">
                        <div className="font-semibold text-foreground">
                          {p.studentName}
                        </div>
                        <div className="text-[10px] text-muted-foreground font-mono">
                          {p.className} · {p.studentCode}
                        </div>
                      </td>

                      <td className="py-2 px-3">
                        <div
                          className="text-foreground truncate max-w-[130px]"
                          title={p.parentName}
                        >
                          {p.parentName}
                        </div>
                        <div className="text-[10px] text-muted-foreground font-mono">
                          {p.parentPhone}
                        </div>
                      </td>

                      <td className="py-2 px-2 text-center">
                        {p.gpa !== null ? (
                          <span
                            className={`font-mono font-bold px-1.5 py-0.5 rounded text-[11px] ${
                              p.gpa >= 10
                                ? "text-status-success bg-status-success/15"
                                : "text-status-danger bg-status-danger/15"
                            }`}
                          >
                            {p.gpa.toFixed(2)}
                          </span>
                        ) : (
                          <span className="text-muted-foreground">—</span>
                        )}
                      </td>

                      <td className="py-2 px-2 text-center font-mono">
                        <div>{(p.attendanceRate * 100).toFixed(0)}%</div>
                        {p.unexcusedAbsences > 0 && (
                          <span className="text-[10px] text-status-danger font-semibold">
                            {p.unexcusedAbsences} abs.
                          </span>
                        )}
                      </td>

                      <td className="py-2 px-3 text-right font-mono">
                        {p.debtAmount > 0 ? (
                          <div>
                            <span className="font-bold text-status-danger">
                              {formatDzdPlain(p.debtAmount)}
                            </span>
                            <span className="text-[10px] text-muted-foreground block">
                              {p.daysOverdue} j
                            </span>
                          </div>
                        ) : (

                        <span className="text-status-success font-medium">
                          0 DA
                        </span>
                      )}
                    </td>

                    <td className="py-2.5 px-3 max-w-[200px]">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        {p.riskCategory === "triple_critical" && (
                          <Badge
                            variant="danger"
                            className="text-[9px] px-1.5 py-0 font-bold"
                          >
                            Triple Risque
                          </Badge>
                        )}
                        <span
                          className="text-[11px] text-muted-foreground truncate block"
                          title={p.primaryRiskReason}
                        >
                          {p.primaryRiskReason}
                        </span>
                      </div>
                    </td>

                    <td className="py-2.5 px-3 text-right">
                      <div className="flex items-center justify-end gap-1">
                        <Button
                          size="sm"
                          variant="ghost"
                          className="h-7 w-7 p-0 text-primary hover:bg-primary/10"
                          onClick={() => handleAskAIAboutStudent(p)}
                          title="Analyser avec l'IA"
                        >
                          <Bot className="h-3.5 w-3.5" />
                        </Button>

                        {p.parentPhone && p.parentPhone !== "—" && (
                          <Button
                            size="sm"
                            variant="ghost"
                            className="h-7 w-7 p-0 text-status-success hover:bg-status-success/10"
                            onClick={() => {
                              const clean = p.parentPhone.replace(/[\s+]/g, "");
                              window.open(`https://wa.me/${clean}`, "_blank");
                            }}
                            title="Contacter par WhatsApp"
                          >
                            <MessageCircle className="h-3.5 w-3.5" />
                          </Button>
                        )}

                        {onOpenStudent && (
                          <Button
                            size="sm"
                            variant="ghost"
                            className="h-7 w-7 p-0 text-muted-foreground hover:text-foreground"
                            onClick={() => onOpenStudent(p.studentId)}
                            title="Ouvrir le dossier élève"
                          >
                            <ExternalLink className="h-3.5 w-3.5" />
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </CardContent>
  </Card>
  );
}
```

---

### Step 13: Redesigning the Alerts Feed (`alerts-tab.tsx`)

This redesign adds an executive notification summary strip at the top, a refined filter toolbar, and unified alert cards with priority pills, status dots, and deep-link drawers.

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/tabs/alerts-tab.tsx
// ============================================================================

import { useEffect, useMemo, useState } from "react";
import {
  Plus,
  Filter,
  ArrowDownUp,
  CheckCheck,
  AlertTriangle,
  Bell,
  Clock,
  ShieldAlert,
  Inbox,
} from "lucide-react";
import { useRepositories } from "../../../app/providers/repository-provider";
import { useAuth } from "../../../app/providers/auth-provider";
import { useToast } from "../../../app/providers/toast-provider";
import type { AppNotification } from "../../../domain/model/operations";
import {
  NOTIFICATION_TYPE_LABELS_FR,
  ALERT_PRIORITY_LABELS_FR,
  ALERT_PRIORITY_TONE,
  ALERT_SOURCE_LABELS_FR,
  sortAlertsByPriority,
} from "../../../domain/model/operations";
import { formatRelative, formatDateTime } from "../../../core/format/date";
import { EmptyState } from "../../../shared/layout/state-views";
import { Card, CardContent } from "../../../shared/ui/card";
import { Button } from "../../../shared/ui/button";
import { Badge } from "../../../shared/ui/badge";
import { StatusChip } from "../../../shared/ui/status-chip";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../../shared/ui/select";
import { AlertCreatorModal } from "../alert-creator-modal";
import { AlertDetailModal } from "../alert-detail-modal";

const SOURCE_LABEL = "Alertes — Manuelle";

export function AlertsTab() {
  const repos = useRepositories();
  const { session } = useAuth();
  const toast = useToast();
  const [items, setItems] = useState<AppNotification[]>([]);
  const [selected, setSelected] = useState<AppNotification | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [creatorOpen, setCreatorOpen] = useState(false);
  const [priorityFilter, setPriorityFilter] = useState<string>("all");
  const [sourceFilter, setSourceFilter] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"priority" | "newest" | "unread">(
    "priority",
  );

  useEffect(() => {
    if (!session) return;
    const unsub = repos.notifications
      .observeForSession({ userId: session.userId, role: session.role })
      .subscribe((n) => {
        setItems([...n]);
      });
    return unsub;
  }, [repos.notifications, session]);

  const filtered = useMemo(() => {
    let list = items;
    if (priorityFilter !== "all")
      list = list.filter((n) => n.priority === priorityFilter);
    if (sourceFilter !== "all")
      list = list.filter((n) => n.source === sourceFilter);
    if (sortBy === "priority") {
      list = sortAlertsByPriority(list);
    } else if (sortBy === "newest") {
      list = [...list].sort((a, b) => b.createdAt.localeCompare(a.createdAt));
    } else if (sortBy === "unread") {
      list = [...list].sort((a, b) => {
        if (!!a.readAt === !b.readAt)
          return b.createdAt.localeCompare(a.createdAt);
        return a.readAt ? 1 : -1;
      });
    }
    return list;
  }, [items, priorityFilter, sourceFilter, sortBy]);

  const counts = useMemo(() => {
    const unread = items.filter((n) => !n.readAt).length;
    const urgent = items.filter((n) => n.priority === "urgent").length;
    const high = items.filter((n) => n.priority === "high").length;
    return { unread, urgent, high, total: items.length };
  }, [items]);

  function openDetail(alert: AppNotification) {
    setSelected(alert);
    setDetailOpen(true);
    if (!alert.readAt) {
      void repos.notifications.markRead(alert.id);
    }
  }

  async function markAllRead() {
    await repos.notifications.markAllRead();
    toast.showSuccess(
      "Alertes marquées",
      `${counts.unread} alerte(s) marquée(s) comme lue(s).`,
    );
  }

  return (
    <div className="space-y-4 pb-8" data-testid="alerts-tab">
      {/* 1. Header Overview Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="rounded-xl border border-border/70 bg-surface-panel p-3.5 flex items-center justify-between shadow-sm">
          <div>
            <span className="text-[10px] font-bold uppercase text-muted-foreground tracking-wider block">
              Total Notifications
            </span>
            <span className="text-xl font-bold font-mono text-foreground tabular-nums">
              {counts.total}
            </span>
          </div>
          <div className="h-8 w-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
            <Bell className="h-4 w-4" />
          </div>
        </div>

        <div className="rounded-xl border border-border/70 bg-surface-panel p-3.5 flex items-center justify-between shadow-sm">
          <div>
            <span className="text-[10px] font-bold uppercase text-muted-foreground tracking-wider block">
              Non Lues
            </span>
            <span className="text-xl font-bold font-mono text-status-warning tabular-nums">
              {counts.unread}
            </span>
          </div>
          <div className="h-8 w-8 rounded-lg bg-status-warning/10 text-status-warning flex items-center justify-center">
            <Clock className="h-4 w-4" />
          </div>
        </div>

        <div className="rounded-xl border border-border/70 bg-surface-panel p-3.5 flex items-center justify-between shadow-sm">
          <div>
            <span className="text-[10px] font-bold uppercase text-muted-foreground tracking-wider block">
              Urgentes
            </span>
            <span className="text-xl font-bold font-mono text-status-danger tabular-nums">
              {counts.urgent}
            </span>
          </div>
          <div className="h-8 w-8 rounded-lg bg-status-danger/10 text-status-danger flex items-center justify-center">
            <ShieldAlert className="h-4 w-4" />
          </div>
        </div>

        <div className="rounded-xl border border-border/70 bg-surface-panel p-3.5 flex items-center justify-between shadow-sm">
          <div>
            <span className="text-[10px] font-bold uppercase text-muted-foreground tracking-wider block">
              Priorité Haute
            </span>
            <span className="text-xl font-bold font-mono text-foreground tabular-nums">
              {counts.high}
            </span>
          </div>
          <div className="h-8 w-8 rounded-lg bg-surface-elevated text-muted-foreground flex items-center justify-center">
            <AlertTriangle className="h-4 w-4" />
          </div>
        </div>
      </div>

      {/* 2. Control Toolbar */}
      <div className="flex items-center justify-between gap-3 flex-wrap rounded-xl border border-border/70 bg-surface-panel p-3 shadow-sm">
        <div className="flex items-center gap-2 flex-wrap">
          <Select value={priorityFilter} onValueChange={setPriorityFilter}>
            <SelectTrigger className="w-36 h-8 text-xs bg-surface-elevated/40">
              <Filter className="h-3 w-3 mr-1" />
              <SelectValue placeholder="Priorité" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Toutes priorités</SelectItem>
              <SelectItem value="urgent">Urgente</SelectItem>
              <SelectItem value="high">Haute</SelectItem>
              <SelectItem value="medium">Moyenne</SelectItem>
              <SelectItem value="low">Basse</SelectItem>
            </SelectContent>
          </Select>

          <Select value={sourceFilter} onValueChange={setSourceFilter}>
            <SelectTrigger className="w-36 h-8 text-xs bg-surface-elevated/40">
              <SelectValue placeholder="Source" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Toutes sources</SelectItem>
              <SelectItem value="system">Système</SelectItem>
              <SelectItem value="manual">Manuelle</SelectItem>
              <SelectItem value="workflow">Workflow</SelectItem>
              <SelectItem value="schedule">Planifiée</SelectItem>
              <SelectItem value="audit">Audit</SelectItem>
            </SelectContent>
          </Select>

          <Select
            value={sortBy}
            onValueChange={(v) => setSortBy(v as typeof sortBy)}
          >
            <SelectTrigger className="w-36 h-8 text-xs bg-surface-elevated/40">
              <ArrowDownUp className="h-3 w-3 mr-1" />
              <SelectValue placeholder="Trier" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="priority">Par priorité</SelectItem>
              <SelectItem value="newest">Plus récentes</SelectItem>
              <SelectItem value="unread">Non lues d'abord</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="flex items-center gap-2">
          {counts.unread > 0 && (
            <Button
              variant="outline"
              size="sm"
              className="h-8 text-xs gap-1.5"
              onClick={markAllRead}
            >
              <CheckCheck className="h-3.5 w-3.5 text-status-success" />
              Tout marquer lu ({counts.unread})
            </Button>
          )}

          <Button
            size="sm"
            className="h-8 text-xs gap-1.5 shadow-sm"
            onClick={() => setCreatorOpen(true)}
          >
            <Plus className="h-3.5 w-3.5" />
            Diffuser une Alerte
          </Button>
        </div>
      </div>

      {/* 3. Alerts Feed */}
      {items.length === 0 ? (
        <EmptyState
          title="Aucune notification enregistrée"
          description="Le journal des alertes est à jour. Vous pouvez diffuser un message ou un rappel si nécessaire."
          icon={<Inbox className="h-8 w-8 text-muted-foreground" />}
        />
      ) : filtered.length === 0 ? (
        <div className="rounded-xl border border-border/70 bg-surface-panel p-12 text-center text-xs text-muted-foreground">
          Aucune alerte ne correspond aux filtres sélectionnés.
        </div>
      ) : (
        <div className="space-y-2.5">
          {filtered.map((n) => {
            const isUnread = !n.readAt;
            const priorityTone = ALERT_PRIORITY_TONE[n.priority];

            return (
              <Card
                key={n.id}
                onClick={() => openDetail(n)}
                className={`cursor-pointer border-border/70 bg-surface-panel hover:bg-surface-elevated/40 transition-all shadow-sm ${
                  isUnread ? "border-l-4 border-l-primary" : ""
                }`}
              >
                <CardContent className="p-3.5 flex items-start gap-3.5">
                  <div className="flex flex-col items-center gap-1 shrink-0 pt-0.5">
                    <StatusChip
                      label={ALERT_PRIORITY_LABELS_FR[n.priority]}
                      tone={priorityTone}
                    />
                    {isUnread && (
                      <span className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
                    )}
                  </div>

                  <div className="flex-1 min-w-0 space-y-1">
                    <div className="flex items-center gap-2 flex-wrap justify-between">
                      <div className="flex items-center gap-2 min-w-0">
                        <span className="text-sm font-bold text-foreground truncate">
                          {n.title}
                        </span>
                        <Badge
                          variant="outline"
                          className="text-[10px] px-1.5 py-0"
                        >
                          {NOTIFICATION_TYPE_LABELS_FR[n.type]}
                        </Badge>
                        <span className="text-[10px] font-mono text-muted-foreground">
                          {ALERT_SOURCE_LABELS_FR[n.source]}
                        </span>
                      </div>
                      <span className="text-[11px] text-muted-foreground font-mono shrink-0">
                        {formatRelative(n.createdAt)}
                      </span>
                    </div>

                    <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2">
                      {n.body}
                    </p>

                    <div className="flex items-center justify-between text-[10px] text-muted-foreground pt-1 border-t border-border/30">
                      <span>Source : {n.sourceLabel}</span>
                      {n.triggeredAt && (
                        <span>Déclenché le {formatDateTime(n.triggeredAt)}</span>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      <AlertCreatorModal
        open={creatorOpen}
        onOpenChange={setCreatorOpen}
        sourceLabel={SOURCE_LABEL}
      />
      <AlertDetailModal
        alert={selected}
        open={detailOpen}
        onOpenChange={setDetailOpen}
      />
    </div>
  );
}
```

---

### Step 14: Redesigning the Global Reports Hub (`reports-tab.tsx`)

This elevates the Reports tab to an institutional documentation center with the featured 13-sheet comprehensive export at the top, followed by cleanly organized macro analytical reports with dual XLSX and PDF capabilities.

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/tabs/reports-tab.tsx
// ============================================================================

import { useState } from "react";
import {
  Users,
  Wallet,
  AlertTriangle,
  TrendingUp,
  ScrollText,
  Loader2,
  FileText,
  Download,
  Database,
  CheckCircle2,
  ArrowRight,
} from "lucide-react";
import { useRepositories } from "../../../app/providers/repository-provider";
import { useToast } from "../../../app/providers/toast-provider";
import { useAuth } from "../../../app/providers/auth-provider";
import { useObservable } from "../../../shared/hooks/use-observable";
import { AuditActions } from "../../../core/audit-actions";
import {
  exportRevenueReport,
  exportOutstandingDebtReport,
  exportStudentRoster,
} from "../../../infrastructure/excel/reports";
import { exportFullWorkbook } from "../../../infrastructure/excel/full-export";
import {
  generateRevenueReportPdf,
  generateOutstandingDebtReportPdf,
  generateStudentRosterPdf,
  generatePersonnelDirectoryPdf,
  generateExpensesByCategoryPdf,
} from "../../../infrastructure/receipt-pdf/global-reports";
import { downloadPdf } from "../../../infrastructure/receipt-pdf/download";
import type { PricingConfig } from "../../../domain/model/pricing";
import { Card, CardContent } from "../../../shared/ui/card";
import { Button } from "../../../shared/ui/button";
import { Badge } from "../../../shared/ui/badge";

export function ReportsTab() {
  const repos = useRepositories();
  const toast = useToast();
  const { session } = useAuth();
  const [exporting, setExporting] = useState<string | null>(null);

  const payments = useObservable(() => repos.payments.observe(), []);
  const debtSummaries = useObservable(() => repos.debt.observeSummary(), []);
  const students = useObservable(() => repos.students.observe(), []);
  const personnel = useObservable(() => repos.personnel.observe(), []);
  const expenses = useObservable(() => repos.expenses.observe(), []);
  const parents = useObservable(() => repos.parents.observe(), []);

  const installments = useObservable(
    () => repos.installments.observe(),
    [],
  );
  const ledger = useObservable(() => repos.ledger.observe(), []);
  const classes = useObservable(() => repos.classes.observe(), []);
  const subjects = useObservable(() => repos.subjects.observe(), []);
  const assessments = useObservable(() => repos.grades.observeAll(), []);
  const attendance = useObservable(
    () =>
      repos.attendance.observeAll("2020-01-01", "2030-12-31"),
    [],
  );
  const pricing = useObservable(() => repos.pricing.observe(), []);

  const pricingValue: PricingConfig | null =
    pricing &&
    (Object.keys(pricing.tuitionByGradeLevel ?? {}).length > 0 ||
      Object.keys(pricing.monthlyByLevel ?? {}).length > 0 ||
      (pricing.registrationFee ?? 0) > 0)
      ? pricing
      : null;

  const standardReports = [
    {
      code: "revenu-mensuel",
      title: "Rapport d'Encaissements Mensuels",
      desc: "Historique complet, ventilation par canal de paiement et ventilation par pôle tarifaire.",
      icon: TrendingUp,
      formats: ["XLSX", "PDF"] as const,
      color: "var(--brand-blue, #349bd4)",
    },
    {
      code: "creances-agees",
      title: "Balance Âgée des Créances",
      desc: "Recensement exhaustif des impayés par famille, coordonnées, jours de retard et sévérité.",
      icon: AlertTriangle,
      formats: ["XLSX", "PDF"] as const,
      color: "var(--status-danger, #ef4444)",
    },
    {
      code: "effectifs-niveau",
      title: "Registre Global des Effectifs",
      desc: "Fichier central des élèves, répartition par cycle, palier académique et classe d'affectation.",
      icon: Users,
      formats: ["XLSX", "PDF"] as const,
      color: "var(--brand-cyan, #3dd6d0)",
    },
    {
      code: "depenses-categorie",
      title: "Journal Analytique des Dépenses",
      desc: "État récapitulatif des décaissements ventilés par catégorie de frais d'exploitation.",
      icon: Wallet,
      formats: ["XLSX", "PDF"] as const,
      color: "var(--brand-gold, #eab308)",
    },
    {
      code: "annuaire-personnel",
      title: "Annuaire du Personnel & Masse Salariale",
      desc: "Effectifs enseignants et personnel administratif, contrats, temps de travail et rémunérations.",
      icon: Users,
      formats: ["XLSX", "PDF"] as const,
      color: "var(--brand-violet, #8b5cf6)",
    },
    {
      code: "journal-audit",
      title: "Registre d'Audit & Traçabilité",
      desc: "Historique d'imputabilité des actions administratives. Accessible depuis Paramètres → Audit.",
      icon: ScrollText,
      formats: ["Voir Settings"] as const,
      color: "var(--brand-slate, #3b464c)",
    },
  ];

  async function handleExport(
    code: string,
    format: "XLSX" | "PDF" | "Voir Settings",
  ) {
    if (format === "Voir Settings") return;
    setExporting(`${code}-${format}`);

    try {
      let exportedRows: number | null = null;
      let fileName = "";

      if (code === "export-complet" && format === "XLSX") {
        fileName = await exportFullWorkbook({
          parents,
          students,
          personnel,
          payments,
          installments,
          ledger,
          expenses,
          assessments,
          subjects,
          attendance,
          debtSummaries,
          classes,
          pricing: pricingValue,
          exportedAt: new Date().toISOString(),
        });
        exportedRows =
          parents.length +
          students.length +
          payments.length +
          ledger.length +
          installments.length;
        toast.showSuccess("Export complet généré", fileName);
      } else if (code === "revenu-mensuel" && format === "XLSX") {
        const today = new Date();
        const from = new Date(today);
        from.setMonth(from.getMonth() - 12);
        await exportRevenueReport(payments, {
          from: from.toISOString().slice(0, 10),
          to: today.toISOString().slice(0, 10),
        });
        exportedRows = payments.length;
      } else if (code === "revenu-mensuel" && format === "PDF") {
        const today = new Date();
        const from = new Date(today);
        from.setMonth(from.getMonth() - 12);
        const bytes = await generateRevenueReportPdf(payments, {
          from: from.toISOString().slice(0, 10),
          to: today.toISOString().slice(0, 10),
        });
        fileName = `el-imtiyaz-revenu-${new Date().toISOString().slice(0, 10)}.pdf`;
        downloadPdf(bytes, fileName);
        exportedRows = payments.length;
        toast.showSuccess("Rapport PDF généré", fileName);
      } else if (code === "creances-agees" && format === "XLSX") {
        const rows = debtSummaries
          .filter((d) => d.outstandingAmount > 0)
          .map((d) => ({
            parentCode:
              parents.find((p) => p.id === d.parentId)?.code ?? d.parentId,
            parentName: d.parentName,
            parentPhone:
              d.parentPhone ||
              parents.find((p) => p.id === d.parentId)?.phone ||
              "",
            bucket: d.bucket as
              | "0_30"
              | "31_60"
              | "61_90"
              | "91_180"
              | "180_plus",
            daysOverdue: d.daysOverdue,
            outstandingAmount: d.outstandingAmount,
          }));
        await exportOutstandingDebtReport(rows, "xlsx");
        exportedRows = rows.length;
      } else if (code === "creances-agees" && format === "PDF") {
        const debtRows = debtSummaries
          .filter((d) => d.outstandingAmount > 0)
          .map((d) => ({
            parentCode:
              parents.find((p) => p.id === d.parentId)?.code ?? d.parentId,
            parentName: d.parentName,
            parentPhone:
              d.parentPhone ||
              parents.find((p) => p.id === d.parentId)?.phone ||
              "",
            bucket: d.bucket as string,
            daysOverdue: d.daysOverdue,
            outstandingAmount: d.outstandingAmount,
          }));
        const bytes = await generateOutstandingDebtReportPdf(debtRows);
        fileName = `el-imtiyaz-creances-${new Date().toISOString().slice(0, 10)}.pdf`;
        downloadPdf(bytes, fileName);
        exportedRows = debtRows.length;
        toast.showSuccess("Rapport PDF généré", fileName);
      } else if (code === "effectifs-niveau" && format === "XLSX") {
        await exportStudentRoster(students);
        exportedRows = students.length;
      } else if (code === "effectifs-niveau" && format === "PDF") {
        const bytes = await generateStudentRosterPdf(students);
        fileName = `el-imtiyaz-effectifs-${new Date().toISOString().slice(0, 10)}.pdf`;
        downloadPdf(bytes, fileName);
        exportedRows = students.length;
        toast.showSuccess("Rapport PDF généré", fileName);
      } else if (code === "annuaire-personnel" && format === "XLSX") {
        if (personnel.length === 0) {
          toast.showWarning("Aucun personnel", "Rien à exporter.");
          return;
        }
        const { exportToXlsx } = await import(
          "../../../infrastructure/excel/export-engine"
        );
        const { STAFF_CATEGORY_LABELS_FR, PERSONNEL_STATUS_LABELS_FR } =
          await import("../../../domain/model/personnel");
        const columns = [
          { header: "Code", key: "code", width: 14 },
          { header: "Prénom", key: "firstName", width: 16 },
          { header: "Nom", key: "lastName", width: 18 },
          { header: "Catégorie", key: "category", width: 18 },
          { header: "Téléphone", key: "phone", width: 18 },
          { header: "E-mail", key: "email", width: 28 },
          { header: "Date d'embauche", key: "hireDate", width: 14 },
          { header: "Statut", key: "status", width: 14 },
          {
            header: "Heures hebdo. cibles",
            key: "weeklyHoursTarget",
            width: 14,
          },
          {
            header: "Heures hebdo. effectuées",
            key: "weeklyHoursLogged",
            width: 14,
          },
          { header: "Salaire (DZD)", key: "salary", width: 16 },
        ];
        const rows = personnel.map((p) => ({
          code: p.id,
          firstName: p.firstName,
          lastName: p.lastName,
          category: STAFF_CATEGORY_LABELS_FR[p.staffCategory],
          phone: p.phone,
          email: p.email ?? "",
          hireDate: p.hireDate,
          status: PERSONNEL_STATUS_LABELS_FR[p.status],
          weeklyHoursTarget: p.weeklyHoursTarget,
          weeklyHoursLogged: p.weeklyHoursLogged,
          salary:
            p.salary != null
              ? new Intl.NumberFormat("fr-FR").format(p.salary)
              : "—",
        }));
        exportToXlsx(
          [{ name: "Personnel", columns, rows }],
          `annuaire-personnel-${new Date().toISOString().slice(0, 10)}.xlsx`,
        );
        toast.showSuccess(
          "Export XLSX",
          `${personnel.length} personnel(s) exporté(s).`,
        );
        return;
      } else if (code === "annuaire-personnel" && format === "PDF") {
        if (personnel.length === 0) {
          toast.showWarning("Aucun personnel", "Rien à exporter.");
          return;
        }
        const bytes = await generatePersonnelDirectoryPdf(personnel);
        fileName = `annuaire-personnel-${new Date().toISOString().slice(0, 10)}.pdf`;
        downloadPdf(bytes, fileName);
        exportedRows = personnel.length;
        toast.showSuccess("Rapport PDF généré", fileName);
      } else if (code === "depenses-categorie" && format === "XLSX") {
        const { exportToXlsx } = await import(
          "../../../infrastructure/excel/export-engine"
        );
        const byCategory = new Map<string, number>();
        for (const e of expenses) {
          byCategory.set(
            e.category,
            (byCategory.get(e.category) ?? 0) + e.amount,
          );
        }
        const columns = [
          { header: "Catégorie", key: "category", width: 24 },
          { header: "Montant total (DZD)", key: "amount", width: 20 },
          { header: "Nombre de dépenses", key: "count", width: 18 },
        ];
        const rows = Array.from(byCategory.entries()).map(([cat, amount]) => ({
          category: cat,
          amount: new Intl.NumberFormat("fr-FR").format(amount),
          count: expenses.filter((e) => e.category === cat).length,
        }));
        exportToXlsx(
          [{ name: "Dépenses par catégorie", columns, rows }],
          `depenses-categorie-${new Date().toISOString().slice(0, 10)}.xlsx`,
        );
        toast.showSuccess(
          "Export XLSX",
          `${byCategory.size} catégories exportées.`,
        );
        return;
      } else if (code === "depenses-categorie" && format === "PDF") {
        const bytes = await generateExpensesByCategoryPdf(expenses);
        fileName = `depenses-categorie-${new Date().toISOString().slice(0, 10)}.pdf`;
        downloadPdf(bytes, fileName);
        exportedRows = expenses.length;
        toast.showSuccess("Rapport PDF généré", fileName);
      }

      if (code !== "export-complet") {
        toast.showSuccess("Export téléchargé", `Fichier généré avec succès.`);
      }

      if (exportedRows !== null) {
        void repos.audit.log({
          action: AuditActions.SystemExport,
          entityType: "report",
          entityId: code,
          actorId: session?.userId ?? "system",
          actorName: session?.displayName ?? "Session courante",
          tenantId: session?.tenantId ?? "mock",
          diff: {
            before: null,
            after: { report: code, format, rows: exportedRows },
          },
          note: `Export ${format} — rapport « ${code} » (${exportedRows} lignes)`,
        });
      }
    } catch (e) {
      toast.showError(
        "Échec de l'export",
        e instanceof Error ? e.message : String(e),
      );
    } finally {
      setExporting(null);
    }
  }

  return (
    <div className="space-y-4 pb-8" data-testid="reports-tab">
      {/* 1. Master Export Banner */}
      <Card className="rounded-xl border border-primary/40 bg-gradient-to-r from-primary/15 via-primary/5 to-surface-panel p-0 overflow-hidden shadow-sm">
        <CardContent className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="h-12 w-12 rounded-xl bg-primary/20 text-primary flex items-center justify-center shrink-0 border border-primary/30 shadow-inner">
              <Database className="h-6 w-6" />
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-foreground">
                  Export Intégral de l'Établissement (Master Workbook)
                </h3>
                <Badge
                  variant="success"
                  className="text-[10px] font-mono px-2"
                >
                  13 Feuilles
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground max-w-2xl leading-relaxed">
                Génération en un clic du classeur Excel complet consolidant :
                Parents, Élèves, Personnel, Paiements, Tranches, Grand Livre,
                Dépenses, Notes, Présences, Créances, Classes et Table tarifaire.
              </p>
            </div>
          </div>

          <Button
            size="default"
            className="gap-2 font-bold shadow-sm whitespace-nowrap self-start md:self-center"
            disabled={exporting === "export-complet-XLSX"}
            onClick={() => handleExport("export-complet", "XLSX")}
          >
            {exporting === "export-complet-XLSX" ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Download className="h-4 w-4" />
            )}
            Télécharger le Classeur (.xlsx)
          </Button>
        </CardContent>
      </Card>

      {/* 2. Standard Analytical Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        {standardReports.map((r) => {
          const Icon = r.icon;
          return (
            <Card
              key={r.code}
              className="rounded-xl border border-border/70 bg-surface-panel hover:border-primary/40 hover:bg-surface-elevated/30 transition-all shadow-sm"
            >
              <CardContent className="p-4 flex flex-col justify-between h-full space-y-4">
                <div className="flex items-start gap-3">
                  <div
                    className="h-10 w-10 rounded-xl flex items-center justify-center shrink-0 border border-border/40"
                    style={{
                      backgroundColor: `${r.color}15`,
                      color: r.color,
                    }}
                  >
                    <Icon className="h-5 w-5" />
                  </div>
                  <div className="space-y-1 min-w-0">
                    <h4 className="text-sm font-bold text-foreground truncate">
                      {r.title}
                    </h4>
                    <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2">
                      {r.desc}
                    </p>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-border/40">
                  <span className="text-[11px] font-mono text-muted-foreground uppercase">
                    Formats disponibles
                  </span>

                  <div className="flex items-center gap-1.5">
                    {r.formats.map((fmt) => {
                      if (fmt === "Voir Settings") {
                        return (
                          <Button
                            key={fmt}
                            variant="ghost"
                            size="sm"
                            className="h-7 text-xs text-primary gap-1"
                            onClick={() =>
                              window.location.assign("/#/settings?tab=audit")
                            }
                          >
                            Ouvrir l'audit
                            <ArrowRight className="h-3 w-3" />
                          </Button>
                        );
                      }

                      const isBusy = exporting === `${r.code}-${fmt}`;

                      return (
                        <Button
                          key={fmt}
                          variant="outline"
                          size="sm"
                          className="h-7 text-xs px-2.5 gap-1 border-border/70"
                          disabled={isBusy}
                          onClick={() => handleExport(r.code, fmt)}
                        >
                          {isBusy ? (
                            <Loader2 className="h-3 w-3 animate-spin" />
                          ) : (
                            <Download className="h-3 w-3" />
                          )}
                          {fmt}
                        </Button>
                      );
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
```

---

### Step 15: Polishing `alert-detail-modal.tsx`

```tsx
// ============================================================================
// FILE: elimtiyaz-desktop/src/features/dashboard/alert-detail-modal.tsx
// ============================================================================

import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bell,
  User as UserIcon,
  Users as UsersIcon,
  Clock,
  Building2,
  Trash2,
  CheckCheck,
  ArrowUpRight,
  AlertTriangle,
  Wallet,
} from "lucide-react";
import { useRepositories } from "../../app/providers/repository-provider";
import { UnifiedModal } from "../../shared/ui/unified-modal";
import { Button } from "../../shared/ui/button";
import { Badge } from "../../shared/ui/badge";
import { Separator } from "../../shared/ui/separator";
import { StatusChip } from "../../shared/ui/status-chip";
import { formatRelative, formatDateTime } from "../../core/format/date";
import {
  ALERT_PRIORITY_LABELS_FR,
  ALERT_PRIORITY_TONE,
  ALERT_SOURCE_LABELS_FR,
  NOTIFICATION_TYPE_LABELS_FR,
  type AppNotification,
} from "../../domain/model/operations";
import { ROLE_LABELS_FR } from "../../core/rbac/roles";
import { UnifiedPaymentModal } from "../../features/financials/unified-payment-modal";
import type { PaymentNavigationContext } from "../../domain/model/payment";
import { parentDisplayName } from "../../domain/model/parent";

export interface AlertDetailModalProps {
  alert: AppNotification | null;
  open: boolean;
  onOpenChange: (o: boolean) => void;
}

export function AlertDetailModal({
  alert,
  open,
  onOpenChange,
}: AlertDetailModalProps) {
  const repos = useRepositories();
  const navigate = useNavigate();
  const [collectOpen, setCollectOpen] = useState(false);

  const linkedEntity = useMemo(() => {
    if (!alert?.entityType || !alert?.entityId) return null;
    switch (alert.entityType) {
      case "parent": {
        const p = repos.parents
          .observe()
          .get()
          .find((x) => x.id === alert.entityId);
        return p
          ? {
              kind: "parent" as const,
              label: parentDisplayName(p),
              subtitle: p.code,
              route: `/crm?parent=${p.id}`,
            }
          : null;
      }
      case "student": {
        const s = repos.students
          .observe()
          .get()
          .find((x) => x.id === alert.entityId);
        return s
          ? {
              kind: "student" as const,
              label: `${s.firstName} ${s.lastName}`,
              subtitle: s.code,
              route: `/crm?student=${s.id}`,
            }
          : null;
      }
      case "expense": {
        const e = repos.expenses
          .observe()
          .get()
          .find((x) => x.id === alert.entityId);
        return e
          ? {
              kind: "expense" as const,
              label: e.title,
              subtitle: e.requestCode,
              route: `/financials?expense=${e.id}`,
            }
          : null;
      }
      case "installment": {
        const parentsList = repos.parents.observe().get();
        let found: { installment: any; parent: any } | null = null;
        for (const p of parentsList) {
          const items = repos.installments.observeByParent(p.id).get();
          const match = items.find((x) => x.id === alert.entityId);
          if (match) {
            found = { installment: match, parent: p };
            break;
          }
        }
        if (!found) return null;
        return {
          kind: "installment" as const,
          label: found.installment.label,
          subtitle: `${found.installment.amountDue.toLocaleString("fr-FR")} DZD`,
          route: `/financials?installment=${found.installment.id}`,
          installment: found.installment,
          parent: found.parent,
        };
      }
      case "homework": {
        return {
          kind: "homework" as const,
          label: "Devoir",
          subtitle: alert.entityId,
          route: `/academics?homework=${alert.entityId}`,
        };
      }
      default:
        return null;
    }
  }, [alert, repos]);

  if (!alert) return null;

  const isInstallmentAlert =
    alert.entityType === "installment" &&
    linkedEntity &&
    (linkedEntity as any).installment;

  const installmentCtx: PaymentNavigationContext | null = isInstallmentAlert
    ? (() => {
        const inst = (linkedEntity as any).installment;
        const parent = (linkedEntity as any).parent;
        const remaining = Math.max(0, inst.amountDue - inst.amountPaid);
        const isOverdue = inst.status === "overdue";
        const overdueDays = isOverdue
          ? Math.max(
              0,
              Math.floor(
                (Date.now() - new Date(inst.dueDate).getTime()) / 86_400_000,
              ),
            )
          : undefined;
        return {
          parentId: inst.parentId,
          parentName: parent ? parentDisplayName(parent) : undefined,
          parentCode: parent?.code,
          studentId: inst.studentId ?? null,
          mode: "installment_tranche" as const,
          targetItemId: inst.id,
          presetAmount: remaining,
          overdueDays,
          dueWindowLabel: new Date(inst.dueDate).toLocaleDateString("fr-FR", {
            day: "numeric",
            month: "short",
            year: "numeric",
          }),
          lineItems: [
            {
              itemId: inst.id,
              category: inst.category,
              label: inst.label,
              grossAmount: inst.amountDue,
              discountAmount: 0,
              netAmount: inst.amountDue,
              alreadyPaidAmount: inst.amountPaid,
              remainingAmount: remaining,
              dueDate: inst.dueDate,
              isOverdue,
              daysOverdue: overdueDays,
            },
          ],
          allowPartial: true,
          originRoute: "dashboard.alert_detail",
        };
      })()
    : null;

  async function handleMarkRead() {
    if (!alert) return;
    await repos.notifications.markRead(alert.id);
    onOpenChange(false);
  }

  async function handleDismiss() {
    if (!alert) return;
    await repos.notifications.dismiss(alert.id);
    onOpenChange(false);
  }

  function handleDeepLink() {
    if (!linkedEntity) return;
    navigate(linkedEntity.route);
    onOpenChange(false);
  }

  const priorityTone = ALERT_PRIORITY_TONE[alert.priority];

  return (
    <>
      <UnifiedModal
        open={open}
        onOpenChange={onOpenChange}
        variant="drawer"
        size="md"
        icon={Bell}
        iconTone={
          priorityTone === "danger"
            ? "danger"
            : priorityTone === "warning"
              ? "warning"
              : "primary"
        }
        title={alert.title}
        description={NOTIFICATION_TYPE_LABELS_FR[alert.type]}
        badge={
          <Badge variant="outline" className="text-[10px]">
            {ALERT_PRIORITY_LABELS_FR[alert.priority]}
          </Badge>
        }
        footer={
          <div className="flex items-center gap-2 w-full justify-between">
            <Button
              variant="ghost"
              size="sm"
              className="text-status-danger hover:bg-status-danger/10 text-xs"
              onClick={handleDismiss}
            >
              <Trash2 className="h-3.5 w-3.5 mr-1" />
              Supprimer
            </Button>

            <div className="flex items-center gap-2">
              {isInstallmentAlert && installmentCtx && (
                <Button
                  size="sm"
                  variant="default"
                  className="text-xs"
                  onClick={() => setCollectOpen(true)}
                >
                  <Wallet className="h-3.5 w-3.5 mr-1" />
                  Encaisser{" "}
                  {installmentCtx.presetAmount
                    ? `${installmentCtx.presetAmount.toLocaleString("fr-FR")} DZD`
                    : ""}
                </Button>
              )}

              {linkedEntity && (
                <Button
                  variant="outline"
                  size="sm"
                  className="text-xs"
                  onClick={handleDeepLink}
                >
                  <ArrowUpRight className="h-3.5 w-3.5 mr-1" />
                  Ouvrir le dossier
                </Button>
              )}

              {!alert.readAt && (
                <Button size="sm" className="text-xs" onClick={handleMarkRead}>
                  <CheckCheck className="h-3.5 w-3.5 mr-1" />
                  Marquer lu
                </Button>
              )}
            </div>
          </div>
        }
      >
        <div className="space-y-4">
          <div className="flex items-center gap-2 flex-wrap">
            <StatusChip
              label={`Priorité ${ALERT_PRIORITY_LABELS_FR[alert.priority]}`}
              tone={priorityTone}
            />
            <StatusChip
              label={ALERT_SOURCE_LABELS_FR[alert.source]}
              tone="neutral"
            />
            <StatusChip label={alert.sourceLabel} tone="info" />
          </div>

          <div className="rounded-xl border border-border/80 bg-surface-elevated/40 p-4">
            <p className="text-sm text-foreground whitespace-pre-wrap leading-relaxed">
              {alert.body}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3 rounded-lg border border-border/50 bg-surface-elevated/20 space-y-1">
              <span className="text-[10px] uppercase font-bold text-muted-foreground block">
                Audience Cible
              </span>
              {alert.targetUserId ? (
                <div className="flex items-center gap-1.5 font-medium">
                  <UserIcon className="h-3.5 w-3.5 text-primary" />
                  <span>Utilisateur spécifique</span>
                </div>
              ) : alert.targetRole ? (
                <div className="flex items-center gap-1.5 font-medium">
                  <UsersIcon className="h-3.5 w-3.5 text-primary" />
                  <span>{ROLE_LABELS_FR[alert.targetRole]}</span>
                </div>
              ) : (
                <div className="flex items-center gap-1.5 font-medium">
                  <UsersIcon className="h-3.5 w-3.5 text-muted-foreground" />
                  <span>Tous les collaborateurs</span>
                </div>
              )}
            </div>

            <div className="p-3 rounded-lg border border-border/50 bg-surface-elevated/20 space-y-1">
              <span className="text-[10px] uppercase font-bold text-muted-foreground block">
                Planification
              </span>
              <div className="flex items-center gap-1.5 font-mono text-muted-foreground">
                <Clock className="h-3.5 w-3.5" />
                <span>
                  {alert.triggeredAt
                    ? formatDateTime(alert.triggeredAt)
                    : "Instantané"}
                </span>
              </div>
            </div>
          </div>

          {linkedEntity && (
            <>
              <Separator />
              <div className="space-y-1.5">
                <span className="text-[10px] uppercase font-bold text-muted-foreground block">
                  Élément Associé
                </span>
                <button
                  type="button"
                  onClick={handleDeepLink}
                  className="flex items-center gap-3 w-full rounded-xl border border-border/70 p-3 hover:bg-surface-elevated/50 transition-colors text-left"
                >
                  <Building2 className="h-5 w-5 text-primary shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-foreground truncate">
                      {linkedEntity.label}
                    </p>
                    <p className="text-[11px] text-muted-foreground font-mono truncate">
                      {linkedEntity.subtitle}
                    </p>
                  </div>
                  <ArrowUpRight className="h-4 w-4 text-muted-foreground shrink-0" />
                </button>
              </div>
            </>
          )}

          {alert.priority === "urgent" && !alert.readAt && (
            <div className="flex items-start gap-2.5 rounded-xl border border-status-danger/40 bg-status-danger/10 p-3 text-xs text-status-danger">
              <AlertTriangle className="h-4 w-4 shrink-0 mt-0.5" />
              <p className="leading-relaxed">
                Notification critique : Cette opération requiert une
                intervention immédiate de la direction.
              </p>
            </div>
          )}

          <Separator />
          <div className="text-[11px] text-muted-foreground space-y-0.5">
            <p>
              Émetteur : <span className="font-mono">{alert.createdBy}</span>
            </p>
            <p>
              Créée {formatRelative(alert.createdAt)} ({formatDateTime(alert.createdAt)})
            </p>
            {alert.readAt && (
              <p>Consultée {formatRelative(alert.readAt)}</p>
            )}
          </div>
        </div>
      </UnifiedModal>

      <UnifiedPaymentModal
        open={collectOpen}
        onOpenChange={setCollectOpen}
        context={installmentCtx}
      />
    </>
  );
}
```

---

### Step 16: Refined Card Glow & Micro-Border Helpers (`index.css`)

Ensure `index.css` includes unified subtle glow transitions and glass surfaces so cards and modals blend into the midnight/dark theme without harsh borders:

```css
/* Add to elimtiyaz-desktop/src/index.css @layer components */

  /* Unified Card Sheen & Border Treatment */
  .dashboard-card {
    background-color: var(--surface-panel);
    border: 1px solid color-mix(in srgb, var(--surface-panel) 60%, hsl(var(--border)));
    border-radius: var(--radius-xl);
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.25);
    transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
  }

  .dashboard-card:hover {
    border-color: color-mix(in srgb, var(--brand-blue) 40%, hsl(var(--border)));
  }

  /* Micro Tonal Card Header */
  .card-header-clean {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid color-mix(in srgb, var(--surface-panel) 70%, hsl(var(--border)));
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
```

---

### Summary of What Was Elevated

1. **Integrated Visual Hierarchy**: All card titles, headers, descriptions, badges, and values now conform to a unified scale:
   - Primary metric numbers: `text-2xl font-bold font-mono tracking-tight tabular-nums`.
   - Small labels: `text-[10px] font-semibold uppercase tracking-wider text-muted-foreground`.
   - Table rows and data cells: clean 12px monospace and readable padding.
2. **Recharts & Visuals Cohesion**: All charts now share the Recharts styling tokens from `DASHBOARD_THEME`: subtle low-contrast gridlines (`rgba(255,255,255,0.06)`), 11px JetBrains Mono axis ticks, glassmorphic tooltips with blur and clean shadows, and consistent bar corner radii `[4, 4, 0, 0]`.
3. **Smooth Cubic-Bezier Sparklines**: The rigid polylines were replaced by mathematically smoothed Catmull-Rom/cubic-bezier SVG paths with linear gradient area fills.
4. **Milestone Wave Cockpit**: `WaveVelocityCard` transformed from plain debug text to an institutional three-stage seasonal cockpit with dual-layer progress meters, status badges, and 2×2 metric grids.
5. **Insights Rail (Zone B)**: Transformed into a real-time actionable command rail with an AI decision card with glowing gradient aura, a high-definition circular progress ring, and a priority relance list with direct WhatsApp and profile shortcuts.
6. **Connected Funnel & Weekly Rhythm**: The recovery funnel is now a connected multi-stage pipeline, and the Algerian school-week chart cleanly stacks Cash, Check, and Wire volumes.
7. **Interactive Operational Calendar**: Fully styled month grid with modern day cells, multi-event indicators, and daily timeline panel.
8. **Consistent Diagnostic & Analysis Tools**: Standardized the Query Console, Triage Radar, Pivot Matrix, Pareto Chart, and YoY comparisons to match the rest of the application.