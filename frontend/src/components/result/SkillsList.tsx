import { Check, X } from "lucide-react"
import { Card } from "@/components/ui/card"

interface Props {
  title: string
  items: string[]
  variant: "matched" | "missing"
}

export function SkillsList({ title, items, variant }: Props) {
  const Icon = variant === "matched" ? Check : X
  const iconClass =
    variant === "matched"
      ? "text-success bg-success/15"
      : "text-destructive bg-destructive/15"

  return (
    <Card className="p-5">
      <div className="mb-3 flex items-center gap-2">
        <div
          className={`flex h-7 w-7 items-center justify-center rounded-full ${iconClass}`}
        >
          <Icon className="h-4 w-4" />
        </div>
        <h3 className="text-sm font-semibold">{title}</h3>
        <span className="ml-auto text-xs text-muted-foreground">
          {items.length}
        </span>
      </div>
      {items.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          {variant === "matched" ? "Eşleşme bulunamadı." : "Eksik tespit edilmedi."}
        </p>
      ) : (
        <ul className="space-y-1.5">
          {items.map((item) => (
            <li
              key={item}
              className="flex items-start gap-2 text-sm text-foreground/90"
            >
              <span className="mt-1.5 inline-block h-1 w-1 shrink-0 rounded-full bg-muted-foreground" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      )}
    </Card>
  )
}
