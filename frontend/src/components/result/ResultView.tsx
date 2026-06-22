import { Card } from "@/components/ui/card"
import { MatchScoreCircle } from "./MatchScoreCircle"
import { SkillsList } from "./SkillsList"
import { GelisimMarkdown } from "./GelisimMarkdown"
import type { AnalysisResponse } from "@/types/api"

interface Props {
  result: AnalysisResponse
}

export function ResultView({ result }: Props) {
  const { match, gelisim_onerileri, baslik } = result

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <div className="mb-1 text-xs uppercase tracking-wider text-muted-foreground">
          Analiz
        </div>
        <h2 className="mb-6 text-xl font-semibold">{baslik}</h2>
        <div className="grid gap-6 md:grid-cols-[auto_1fr] md:gap-8">
          <MatchScoreCircle score={match.uyum_puani} />
          <div>
            <h3 className="mb-2 text-sm font-semibold">Genel Değerlendirme</h3>
            <p className="text-sm leading-relaxed text-muted-foreground">
              {match.genel_degerlendirme}
            </p>
          </div>
        </div>
        {match.deneyim_uyumu && (
          <div className="mt-6 border-t pt-4">
            <h3 className="mb-2 text-sm font-semibold">Tecrübe Uyumu</h3>
            <p className="text-sm leading-relaxed text-muted-foreground">
              {match.deneyim_uyumu}
            </p>
          </div>
        )}
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <SkillsList
          title="Eşleşen Beceriler"
          items={match.eslesen_beceriler}
          variant="matched"
        />
        <SkillsList
          title="Eksik Beceriler"
          items={match.eksik_beceriler}
          variant="missing"
        />
      </div>

      <GelisimMarkdown markdown={gelisim_onerileri} />
    </div>
  )
}
