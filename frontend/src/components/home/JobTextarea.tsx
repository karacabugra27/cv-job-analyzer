import { Card } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"

interface Props {
  value: string
  onChange: (v: string) => void
}

export function JobTextarea({ value, onChange }: Props) {
  return (
    <Card className="p-4">
      <div className="mb-2 flex items-center justify-between">
        <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          İş Tanımı
        </label>
        <span className="text-xs text-muted-foreground">
          {value.length} karakter
        </span>
      </div>
      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Başvurmak istediğiniz iş ilanının tüm metnini buraya yapıştırın: pozisyon, sorumluluklar, aranan nitelikler, teknik gereksinimler..."
        className="min-h-[180px] border-0 px-0 focus-visible:ring-0 focus-visible:ring-offset-0"
      />
    </Card>
  )
}
