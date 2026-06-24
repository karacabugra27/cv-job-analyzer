import { useEffect, useState } from "react"
import { Bug, Lightbulb, MessageSquare, MessagesSquare, X } from "lucide-react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { cn } from "@/lib/utils"
import { sendFeedback, type FeedbackCategory } from "@/lib/api"
import { useAuth } from "@/lib/auth"

type Option = {
  value: FeedbackCategory
  label: string
  description: string
  Icon: typeof Bug
}

const options: Option[] = [
  {
    value: "bug",
    label: "Hata bildir",
    description: "Bir şey beklediğin gibi çalışmıyor.",
    Icon: Bug,
  },
  {
    value: "idea",
    label: "Öneri",
    description: "Eklenmesini istediğin bir özellik var.",
    Icon: Lightbulb,
  },
  {
    value: "other",
    label: "Diğer",
    description: "Genel bir geri bildirim.",
    Icon: MessageSquare,
  },
]

export function FeedbackButton() {
  const { session } = useAuth()
  const [open, setOpen] = useState(false)
  const [category, setCategory] = useState<FeedbackCategory>("idea")
  const [message, setMessage] = useState("")
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false)
    }
    document.addEventListener("keydown", onKey)
    return () => document.removeEventListener("keydown", onKey)
  }, [open])

  if (!session) return null

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (message.trim().length < 3) {
      toast.error("Lütfen biraz daha açıklayıcı yaz.")
      return
    }
    setSubmitting(true)
    try {
      await sendFeedback({
        category,
        message: message.trim(),
        page_url: window.location.href,
      })
      toast.success("Teşekkürler! Geri bildirimini aldık.")
      setMessage("")
      setOpen(false)
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Bir şeyler ters gitti.")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="fixed bottom-5 right-5 z-30 flex items-center gap-2 rounded-full bg-primary px-4 py-3 text-sm font-medium text-primary-foreground shadow-lg transition-opacity hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
        aria-label="Geri bildirim gönder"
      >
        <MessagesSquare className="h-4 w-4" />
        <span className="hidden sm:inline">Geri bildirim</span>
      </button>

      {open && (
        <div
          className="fixed inset-0 z-40 flex items-end justify-center bg-black/40 p-4 backdrop-blur-sm sm:items-center"
          onClick={() => setOpen(false)}
        >
          <div
            role="dialog"
            aria-modal="true"
            aria-label="Geri bildirim formu"
            className="w-full max-w-md rounded-xl border border-border bg-background p-6 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-4 flex items-start justify-between gap-3">
              <div>
                <h2 className="text-lg font-semibold">Geri bildirim gönder</h2>
                <p className="text-sm text-muted-foreground">
                  Hatalar, öneriler ve eksik gördüklerini bize ulaştır.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="rounded-md p-1 text-muted-foreground hover:bg-secondary"
                aria-label="Kapat"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div
                role="radiogroup"
                aria-label="Geri bildirim türü"
                className="grid grid-cols-3 gap-2"
              >
                {options.map((opt) => {
                  const Icon = opt.Icon
                  const active = category === opt.value
                  return (
                    <button
                      key={opt.value}
                      type="button"
                      role="radio"
                      aria-checked={active}
                      onClick={() => setCategory(opt.value)}
                      className={cn(
                        "flex flex-col items-center gap-1 rounded-md border px-2 py-3 text-xs transition-colors",
                        active
                          ? "border-primary bg-primary/10 text-foreground"
                          : "border-border text-muted-foreground hover:bg-secondary"
                      )}
                    >
                      <Icon className="h-4 w-4" />
                      {opt.label}
                    </button>
                  )
                })}
              </div>

              <p className="text-xs text-muted-foreground">
                {options.find((o) => o.value === category)?.description}
              </p>

              <Textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Ne yaşadın, ne öneriyorsun? Mümkünse adımları da yaz."
                maxLength={4000}
                autoFocus
              />

              <div className="flex items-center justify-between gap-3">
                <span className="text-xs text-muted-foreground">
                  {message.length}/4000
                </span>
                <div className="flex gap-2">
                  <Button
                    type="button"
                    variant="ghost"
                    onClick={() => setOpen(false)}
                    disabled={submitting}
                  >
                    Vazgeç
                  </Button>
                  <Button type="submit" disabled={submitting}>
                    {submitting ? "Gönderiliyor..." : "Gönder"}
                  </Button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}
