import { Card } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

export function ResultSkeleton() {
  return (
    <div className="space-y-6">
      <Card className="p-6">
        <Skeleton className="mb-4 h-4 w-1/3" />
        <div className="grid gap-6 md:grid-cols-[auto_1fr] md:gap-8">
          <Skeleton className="h-40 w-40 rounded-full" />
          <div className="space-y-2">
            <Skeleton className="h-4 w-2/3" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-3/4" />
          </div>
        </div>
      </Card>
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="space-y-2 p-5">
          <Skeleton className="h-5 w-1/2" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-4/6" />
        </Card>
        <Card className="space-y-2 p-5">
          <Skeleton className="h-5 w-1/2" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-4/6" />
        </Card>
      </div>
      <Card className="space-y-3 p-6">
        <Skeleton className="h-5 w-1/3" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
      </Card>
    </div>
  )
}
