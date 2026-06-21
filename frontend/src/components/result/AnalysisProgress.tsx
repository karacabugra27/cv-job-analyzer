import { useEffect, useState } from "react"
import { Check, Loader2, Sparkles } from "lucide-react"
import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"

type Step = {
  title: string
  description: string
  duration: number
}

const STEPS: Step[] = [
  {
    title: "CV içeriği işleniyor",
    description: "Yetkinlikler, deneyim ve eğitim çıkarılıyor.",
    duration: 9000,
  },
  {
    title: "İş tanımı çözümleniyor",
    description: "Aranan nitelikler ve sorumluluklar ayrıştırılıyor.",
    duration: 8000,
  },
  {
    title: "Uyum skoru hesaplanıyor",
    description: "Gereksinimler CV ile eşleştirilip puanlanıyor.",
    duration: 14000,
  },
  {
    title: "Gelişim önerileri yazılıyor",
    description: "Eksiklere yönelik somut adımlar oluşturuluyor.",
    duration: 14000,
  },
]

const TOTAL_DURATION = STEPS.reduce((sum, s) => sum + s.duration, 0)

export function AnalysisProgress({ isDone = false }: { isDone?: boolean }) {
  const [elapsed, setElapsed] = useState(0)

  useEffect(() => {
    const start = Date.now()
    const tick = setInterval(() => {
      setElapsed(Date.now() - start)
    }, 200)
    return () => clearInterval(tick)
  }, [])

  let activeIndex = STEPS.length - 1
  let cum = 0
  for (let i = 0; i < STEPS.length; i++) {
    cum += STEPS[i].duration
    if (elapsed < cum) {
      activeIndex = i
      break
    }
  }

  const progressPct = isDone
    ? 100
    : Math.min(99, (elapsed / TOTAL_DURATION) * 100)

  return (
    <Card className="overflow-hidden p-6 md:p-8">
      <div className="mb-5 flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
            Analiz sürüyor
          </p>
          <h3 className="mt-1 text-2xl font-semibold tracking-tight">
            Kariyer koçu çalışıyor...
          </h3>
        </div>
        <div className="relative flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-primary/20 to-primary/5 ring-1 ring-primary/30">
          <Sparkles className="h-5 w-5 text-primary animate-pulse" />
          <span className="absolute inset-0 animate-ping rounded-full bg-primary/10" />
        </div>
      </div>

      <div className="mb-6 h-1.5 w-full overflow-hidden rounded-full bg-secondary">
        <div
          className="h-full rounded-full bg-primary transition-all duration-300 ease-out"
          style={{ width: `${progressPct}%` }}
        />
      </div>

      <ol className="space-y-2">
        {STEPS.map((step, idx) => {
          const isComplete = isDone || idx < activeIndex
          const isActive = !isDone && idx === activeIndex
          return (
            <li
              key={idx}
              className={cn(
                "flex items-start gap-3 rounded-lg border p-3 transition-colors",
                isActive
                  ? "border-primary/30 bg-primary/5"
                  : "border-transparent"
              )}
            >
              <div
                className={cn(
                  "mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full transition-colors",
                  isComplete
                    ? "bg-primary text-primary-foreground"
                    : isActive
                      ? "text-primary"
                      : "text-muted-foreground/40"
                )}
              >
                {isComplete ? (
                  <Check className="h-4 w-4" strokeWidth={3} />
                ) : isActive ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <span className="h-2.5 w-2.5 rounded-full border-2 border-current" />
                )}
              </div>
              <div className="flex-1">
                <p
                  className={cn(
                    "text-sm font-medium leading-tight",
                    isComplete || isActive
                      ? "text-foreground"
                      : "text-muted-foreground"
                  )}
                >
                  {step.title}
                </p>
                <p
                  className={cn(
                    "mt-1 text-xs leading-snug",
                    isActive
                      ? "text-muted-foreground"
                      : "text-muted-foreground/70"
                  )}
                >
                  {step.description}
                </p>
                {isActive && (
                  <div className="mt-2 flex gap-1">
                    {[0, 1, 2].map((i) => (
                      <span
                        key={i}
                        className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary/60"
                        style={{ animationDelay: `${i * 0.15}s` }}
                      />
                    ))}
                  </div>
                )}
              </div>
            </li>
          )
        })}
      </ol>
    </Card>
  )
}
