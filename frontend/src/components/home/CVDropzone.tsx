import { useCallback, useRef, useState } from "react"
import { Upload, FileText, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface Props {
  file: File | null
  onChange: (file: File | null) => void
}

const MAX_SIZE = 5 * 1024 * 1024 // 5MB

export function CVDropzone({ file, onChange }: Props) {
  const [drag, setDrag] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = useCallback(
    (f: File | null) => {
      setError(null)
      if (!f) {
        onChange(null)
        return
      }
      if (f.type !== "application/pdf") {
        setError("Sadece PDF dosyası kabul edilir.")
        return
      }
      if (f.size > MAX_SIZE) {
        setError("Maksimum dosya boyutu 5MB.")
        return
      }
      onChange(f)
    },
    [onChange]
  )

  return (
    <Card
      onDragOver={(e) => {
        e.preventDefault()
        setDrag(true)
      }}
      onDragLeave={() => setDrag(false)}
      onDrop={(e) => {
        e.preventDefault()
        setDrag(false)
        handleFile(e.dataTransfer.files?.[0] ?? null)
      }}
      className={cn(
        "flex flex-col items-center justify-center gap-3 border-dashed p-10 transition-colors",
        drag && "border-primary bg-primary/5",
        file && "border-solid border-success/40 bg-success/5"
      )}
    >
      {file ? (
        <>
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-success/15">
            <FileText className="h-5 w-5 text-success" />
          </div>
          <div className="text-center">
            <p className="text-sm font-medium">{file.name}</p>
            <p className="text-xs text-muted-foreground">
              {(file.size / 1024).toFixed(0)} KB · PDF
            </p>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => handleFile(null)}
            className="gap-1.5"
          >
            <X className="h-3.5 w-3.5" /> Kaldır
          </Button>
        </>
      ) : (
        <>
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-muted">
            <Upload className="h-5 w-5 text-muted-foreground" />
          </div>
          <div className="text-center">
            <p className="text-sm font-medium">CV'nizi buraya sürükleyin</p>
            <p className="text-xs text-muted-foreground">
              Maksimum 5MB · sadece PDF
            </p>
          </div>
          <Button
            variant="default"
            size="sm"
            onClick={() => inputRef.current?.click()}
          >
            Dosya Seç
          </Button>
        </>
      )}
      {error && <p className="text-xs text-destructive">{error}</p>}
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
      />
    </Card>
  )
}
