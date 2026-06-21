import { useState } from "react"
import { Navigate, useLocation } from "react-router-dom"
import { toast } from "sonner"
import { supabase } from "@/lib/supabase"
import { useAuth } from "@/lib/auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { GoogleIcon } from "@/components/icons/GoogleIcon"
import { Logo } from "@/components/layout/Logo"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export function LoginPage() {
  const { session, loading } = useAuth()
  const location = useLocation()
  const [mode, setMode] = useState<"login" | "signup">("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [submitting, setSubmitting] = useState(false)

  if (loading) return null
  if (session) {
    const from = (location.state as { from?: string } | null)?.from ?? "/"
    return <Navigate to={from} replace />
  }

  async function handleEmailSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    try {
      if (mode === "login") {
        const { error } = await supabase.auth.signInWithPassword({
          email,
          password,
        })
        if (error) throw error
        toast.success("Giriş başarılı")
      } else {
        const { error } = await supabase.auth.signUp({ email, password })
        if (error) throw error
        toast.success("Kayıt tamam — e-postanı kontrol et.")
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Bir hata oluştu"
      toast.error(msg)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleGoogle() {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: window.location.origin },
    })
    if (error) toast.error(error.message)
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center px-6 py-12">
      <div className="mb-8">
        <Logo />
      </div>
      <Card className="w-full">
        <CardHeader>
          <CardTitle>{mode === "login" ? "Giriş yap" : "Hesap oluştur"}</CardTitle>
          <CardDescription>
            Analiz yapmak için hesabına giriş yapmalısın.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={handleEmailSubmit} className="space-y-3">
            <Input
              type="email"
              placeholder="E-posta"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
            <Input
              type="password"
              placeholder="Şifre"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
              autoComplete={mode === "login" ? "current-password" : "new-password"}
            />
            <Button type="submit" className="w-full" disabled={submitting}>
              {mode === "login" ? "Giriş yap" : "Kayıt ol"}
            </Button>
          </form>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t border-border" />
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="bg-card px-2 text-muted-foreground">veya</span>
            </div>
          </div>

          <Button
            type="button"
            variant="outline"
            className="w-full gap-2"
            onClick={handleGoogle}
          >
            <GoogleIcon className="h-4 w-4" />
            Google ile devam et
          </Button>

          <p className="text-center text-sm text-muted-foreground">
            {mode === "login" ? "Hesabın yok mu?" : "Zaten hesabın var mı?"}{" "}
            <button
              type="button"
              className="font-medium text-foreground hover:underline"
              onClick={() => setMode(mode === "login" ? "signup" : "login")}
            >
              {mode === "login" ? "Kayıt ol" : "Giriş yap"}
            </button>
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
