import { Sparkles } from "lucide-react"

export function Logo() {
  return (
    <div className="flex items-center gap-2">
      <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary text-primary-foreground">
        <Sparkles className="h-4 w-4" />
      </div>
      <span className="text-base font-semibold tracking-tight">Liyakat AI</span>
    </div>
  )
}
