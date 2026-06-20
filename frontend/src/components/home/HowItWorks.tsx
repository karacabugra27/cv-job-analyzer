import { Card } from "@/components/ui/card"

const steps = [
  {
    n: "01",
    title: "CV'nizi yükleyin",
    desc: "PDF olarak özgeçmişinizi sürükleyip bırakın.",
  },
  {
    n: "02",
    title: "İlanı yapıştırın",
    desc: "Başvuracağınız iş tanımının tüm metnini ekleyin.",
  },
  {
    n: "03",
    title: "Analizinizi alın",
    desc: "Skor, güçlü yönler, eksikler ve plan saniyeler içinde.",
  },
]

export function HowItWorks() {
  return (
    <Card className="p-6">
      <p className="mb-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Nasıl çalışır?
      </p>
      <ol className="space-y-4">
        {steps.map((s) => (
          <li key={s.n} className="flex gap-3">
            <span className="text-xs font-semibold text-primary">{s.n}</span>
            <div>
              <p className="text-sm font-medium">{s.title}</p>
              <p className="text-xs text-muted-foreground">{s.desc}</p>
            </div>
          </li>
        ))}
      </ol>
    </Card>
  )
}
