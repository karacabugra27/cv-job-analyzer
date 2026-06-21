import { useAuth } from "@/lib/auth"

export function Footer() {
  const { session } = useAuth()
  if (!session) return null

  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-6xl flex-col items-start gap-2 px-6 py-6 text-xs text-muted-foreground md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-2">
          <span className="inline-block h-2 w-2 rounded-full bg-primary" />
          <span>© 2026 Liyakat — Türkçe kariyer koçu</span>
        </div>
        <div>
          CV ve iş tanımı verileriniz yalnızca analiz için kullanılır,
          saklanmaz.
        </div>
      </div>
    </footer>
  )
}
