import { cn } from "@/lib/utils"

interface Props {
  score: number
  size?: number
}

function scoreColor(score: number): string {
  if (score >= 75) return "text-success"
  if (score >= 50) return "text-primary"
  return "text-destructive"
}

function scoreLabel(score: number): string {
  if (score >= 80) return "Mükemmel uyum"
  if (score >= 65) return "İyi uyum"
  if (score >= 45) return "Orta uyum"
  return "Düşük uyum"
}

export function MatchScoreCircle({ score, size = 160 }: Props) {
  const radius = (size - 16) / 2
  const circumference = 2 * Math.PI * radius
  const dash = (score / 100) * circumference
  const color = scoreColor(score)

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            strokeWidth={10}
            className="stroke-muted"
            fill="none"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            strokeWidth={10}
            strokeLinecap="round"
            className={cn("transition-all duration-700", color)}
            stroke="currentColor"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={circumference - dash}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={cn("text-4xl font-bold tabular-nums", color)}>
            {score}
          </span>
          <span className="text-xs text-muted-foreground">/ 100</span>
        </div>
      </div>
      <p className={cn("text-sm font-medium", color)}>{scoreLabel(score)}</p>
    </div>
  )
}
