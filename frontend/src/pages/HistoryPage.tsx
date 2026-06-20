import { Link } from "react-router-dom"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { ArrowRight, Trash2, Loader2, FileText } from "lucide-react"
import { toast } from "sonner"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { fetchHistory, deleteHistory } from "@/lib/api"

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleString("tr-TR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  } catch {
    return iso
  }
}

function scoreBadgeVariant(score: number | null) {
  if (score === null) return "muted" as const
  if (score >= 75) return "success" as const
  if (score >= 50) return "default" as const
  return "outline" as const
}

export function HistoryPage() {
  const qc = useQueryClient()
  const { data, isLoading, error } = useQuery({
    queryKey: ["history"],
    queryFn: fetchHistory,
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteHistory(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["history"] })
      toast.success("Analiz silindi")
    },
    onError: () => toast.error("Silinemedi"),
  })

  return (
    <div className="mx-auto max-w-6xl px-6 py-10 md:py-16">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold tracking-tight">
          Geçmiş analizler
        </h1>
        <p className="text-sm text-muted-foreground">
          Daha önce yaptığınız tüm analizler.
        </p>
      </div>

      {isLoading && (
        <div className="flex items-center justify-center py-20 text-muted-foreground">
          <Loader2 className="h-5 w-5 animate-spin" />
        </div>
      )}

      {error && (
        <Card className="p-6 text-sm text-destructive">
          Geçmiş yüklenemedi: {(error as Error).message}
        </Card>
      )}

      {data && data.items.length === 0 && (
        <Card className="flex flex-col items-center justify-center gap-3 p-12 text-center">
          <FileText className="h-8 w-8 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">
            Henüz analiz yapmadınız.
          </p>
          <Button asChild>
            <Link to="/">İlk analizi başlat</Link>
          </Button>
        </Card>
      )}

      {data && data.items.length > 0 && (
        <ul className="space-y-3">
          {data.items.map((item) => (
            <li key={item.id}>
              <Card className="flex items-center gap-4 p-5">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h3 className="text-base font-semibold">{item.baslik}</h3>
                    {item.uyum_puani !== null && (
                      <Badge variant={scoreBadgeVariant(item.uyum_puani)}>
                        {item.uyum_puani}/100
                      </Badge>
                    )}
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {formatDate(item.tarih)}
                  </p>
                </div>
                <Button asChild variant="ghost" size="sm">
                  <Link to={`/history/${item.id}`}>
                    Detay <ArrowRight className="h-3.5 w-3.5" />
                  </Link>
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => deleteMutation.mutate(item.id)}
                  disabled={deleteMutation.isPending}
                  aria-label="Sil"
                >
                  <Trash2 className="h-4 w-4 text-destructive" />
                </Button>
              </Card>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
