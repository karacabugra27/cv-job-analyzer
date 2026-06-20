import { Link, useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { ArrowLeft, Loader2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ResultView } from "@/components/result/ResultView"
import { fetchHistoryDetail } from "@/lib/api"

export function HistoryDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, error } = useQuery({
    queryKey: ["history", id],
    queryFn: () => fetchHistoryDetail(id!),
    enabled: !!id,
  })

  return (
    <div className="mx-auto max-w-6xl px-6 py-10 md:py-16">
      <Button asChild variant="ghost" size="sm" className="mb-6 -ml-3">
        <Link to="/history">
          <ArrowLeft className="h-4 w-4" /> Geçmişe dön
        </Link>
      </Button>

      {isLoading && (
        <div className="flex items-center justify-center py-20 text-muted-foreground">
          <Loader2 className="h-5 w-5 animate-spin" />
        </div>
      )}

      {error && (
        <Card className="p-6 text-sm text-destructive">
          Analiz yüklenemedi: {(error as Error).message}
        </Card>
      )}

      {data && <ResultView result={data} />}
    </div>
  )
}
