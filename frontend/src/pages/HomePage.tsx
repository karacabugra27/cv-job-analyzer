import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { ArrowRight, Loader2 } from "lucide-react"
import { toast } from "sonner"

import { Hero } from "@/components/home/Hero"
import { CVDropzone } from "@/components/home/CVDropzone"
import { JobTextarea } from "@/components/home/JobTextarea"
import { InfoCard } from "@/components/home/InfoCard"
import { HowItWorks } from "@/components/home/HowItWorks"
import { AnalysisProgress } from "@/components/result/AnalysisProgress"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { analyze } from "@/lib/api"

export function HomePage() {
  const [cvFile, setCvFile] = useState<File | null>(null)
  const [jobText, setJobText] = useState("")
  const [baslik, setBaslik] = useState("")
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: async () => {
      if (!cvFile) throw new Error("CV yükleyin")
      if (!jobText.trim()) throw new Error("İş tanımını yapıştırın")
      if (!baslik.trim()) throw new Error("Analiz başlığı girin")
      return analyze(cvFile, jobText, baslik)
    },
    onSuccess: (data) => {
      queryClient.setQueryData(["history", data.id], data)
      queryClient.invalidateQueries({ queryKey: ["history"] })
      toast.success("Analiz tamamlandı")
      navigate(`/history/${data.id}`)
    },
    onError: (err: Error) => {
      toast.error(err.message || "Bir hata oluştu")
    },
  })

  return (
    <div className="mx-auto max-w-6xl px-6 py-10 md:py-16">
      <div className="mb-12">
        <Hero />
      </div>

      <div className="grid gap-6 md:grid-cols-[1.4fr_1fr]">
        {/* Sol: Form */}
        <div className="space-y-4">
          <CVDropzone file={cvFile} onChange={setCvFile} />
          <JobTextarea value={jobText} onChange={setJobText} />
          <Input
            placeholder="Analiz başlığı"
            value={baslik}
            onChange={(e) => setBaslik(e.target.value)}
          />
          <Button
            size="lg"
            className="w-full gap-2"
            onClick={() => mutation.mutate()}
            disabled={mutation.isPending}
          >
            {mutation.isPending ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Analiz ediliyor...
              </>
            ) : (
              <>
                Analiz Et <ArrowRight className="h-4 w-4" />
              </>
            )}
          </Button>
        </div>

        {/* Sağ: Info + How */}
        <div className="space-y-4">
          {mutation.isPending ? (
            <AnalysisProgress />
          ) : (
            <>
              <InfoCard />
              <HowItWorks />
            </>
          )}
        </div>
      </div>
    </div>
  )
}
