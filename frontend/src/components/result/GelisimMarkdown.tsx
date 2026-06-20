import ReactMarkdown from "react-markdown"
import { Card } from "@/components/ui/card"
import { TrendingUp } from "lucide-react"

interface Props {
  markdown: string
}

export function GelisimMarkdown({ markdown }: Props) {
  return (
    <Card className="p-6">
      <div className="mb-4 flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <TrendingUp className="h-4 w-4" />
        </div>
        <h3 className="text-base font-semibold">Gelişim Planınız</h3>
      </div>
      <div className="prose-content text-sm leading-relaxed">
        <ReactMarkdown
          components={{
            h1: ({ children }) => (
              <h1 className="mb-3 mt-6 text-lg font-semibold first:mt-0">
                {children}
              </h1>
            ),
            h2: ({ children }) => (
              <h2 className="mb-2 mt-5 text-base font-semibold first:mt-0">
                {children}
              </h2>
            ),
            h3: ({ children }) => (
              <h3 className="mb-2 mt-4 text-sm font-semibold first:mt-0">
                {children}
              </h3>
            ),
            p: ({ children }) => (
              <p className="mb-3 text-foreground/90">{children}</p>
            ),
            ul: ({ children }) => (
              <ul className="mb-3 space-y-1.5 pl-5 [&>li]:list-disc">
                {children}
              </ul>
            ),
            ol: ({ children }) => (
              <ol className="mb-3 space-y-1.5 pl-5 [&>li]:list-decimal">
                {children}
              </ol>
            ),
            li: ({ children }) => (
              <li className="text-foreground/90">{children}</li>
            ),
            strong: ({ children }) => (
              <strong className="font-semibold text-foreground">
                {children}
              </strong>
            ),
            code: ({ children }) => (
              <code className="rounded bg-muted px-1.5 py-0.5 text-xs">
                {children}
              </code>
            ),
          }}
        >
          {markdown}
        </ReactMarkdown>
      </div>
    </Card>
  )
}
