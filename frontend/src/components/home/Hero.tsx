import { Sparkles } from "lucide-react"
import { Badge } from "@/components/ui/badge"

export function Hero() {
  return (
    <div className="flex flex-col gap-6">
      <Badge variant="outline" className="self-start gap-1.5">
        <Sparkles className="h-3.5 w-3.5 text-primary" />
        Yapay zeka destekli kariyer koçu
      </Badge>

      <h1 className="text-4xl font-bold leading-tight tracking-tight md:text-5xl">
        Kariyer hedeflerinize{" "}
        <span className="italic text-primary">veriye dayalı</span> adımlarla
        ilerleyin
      </h1>

      <p className="max-w-xl text-base text-muted-foreground">
        CV'nizi yükleyin ve başvuracağınız iş ilanını yapıştırın. Saniyeler
        içinde uyum skorunuzu, güçlü yönlerinizi, eksiklerinizi ve kişisel
        gelişim önerilerinizi görün.
      </p>
    </div>
  )
}
