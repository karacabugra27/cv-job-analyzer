import { Sparkles, Check } from "lucide-react"
import { Card } from "@/components/ui/card"

const points = [
  "Veriye dayalı uyum skoru",
  "Tam karşılanan gereksinimler",
  "Eksik kalan kritik noktalar",
  "Adım adım gelişim planı",
]

export function InfoCard() {
  return (
    <Card className="p-6">
      <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
        <Sparkles className="h-5 w-5" />
      </div>
      <h3 className="mb-2 text-base font-semibold">
        Analiziniz burada belirecek
      </h3>
      <p className="mb-4 text-sm text-muted-foreground">
        CV'nizi yükleyin ve iş tanımını yapıştırın. Kariyer koçunuz size 0–100
        arası bir uyum skoru, güçlü yönleriniz, eksiklikleriniz ve somut
        gelişim önerileri sunacak.
      </p>
      <ul className="space-y-2">
        {points.map((p) => (
          <li
            key={p}
            className="flex items-start gap-2 text-sm text-muted-foreground"
          >
            <Check className="mt-0.5 h-4 w-4 shrink-0 text-success" />
            <span>{p}</span>
          </li>
        ))}
      </ul>
    </Card>
  )
}
