import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useMutation } from "@tanstack/react-query"
import { toast } from "sonner"
import { Mail, ShieldCheck, Trash2, User as UserIcon } from "lucide-react"

import { supabase } from "@/lib/supabase"
import { deleteAccount } from "@/lib/api"
import { useAuth } from "@/lib/auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

function formatDate(iso: string | undefined) {
  if (!iso) return "—"
  try {
    return new Date(iso).toLocaleDateString("tr-TR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    })
  } catch {
    return iso
  }
}

export function ProfilePage() {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()
  const displayNameInitial =
    (user?.user_metadata?.full_name as string | undefined) ?? ""
  const [fullName, setFullName] = useState(displayNameInitial)
  const [password, setPassword] = useState("")
  const [passwordConfirm, setPasswordConfirm] = useState("")
  const [confirmingDelete, setConfirmingDelete] = useState(false)

  const nameMutation = useMutation({
    mutationFn: async () => {
      const { error } = await supabase.auth.updateUser({
        data: { full_name: fullName.trim() },
      })
      if (error) throw error
    },
    onSuccess: () => toast.success("İsim güncellendi"),
    onError: (err: Error) => toast.error(err.message),
  })

  const passwordMutation = useMutation({
    mutationFn: async () => {
      if (password.length < 6) throw new Error("Şifre en az 6 karakter olmalı")
      if (password !== passwordConfirm) throw new Error("Şifreler eşleşmiyor")
      const { error } = await supabase.auth.updateUser({ password })
      if (error) throw error
    },
    onSuccess: () => {
      toast.success("Şifren güncellendi")
      setPassword("")
      setPasswordConfirm("")
    },
    onError: (err: Error) => toast.error(err.message),
  })

  const deleteMutation = useMutation({
    mutationFn: deleteAccount,
    onSuccess: async () => {
      toast.success("Hesabın silindi")
      await signOut()
      navigate("/login", { replace: true })
    },
    onError: (err: Error) => toast.error(err.message),
  })

  const provider = (user?.app_metadata?.provider as string | undefined) ?? "email"
  const isOAuth = provider !== "email"

  return (
    <div className="mx-auto max-w-3xl px-6 py-10 md:py-16">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight">Profil</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Hesap bilgilerini ve güvenlik ayarlarını yönet.
        </p>
      </div>

      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <UserIcon className="h-4 w-4" />
              Hesap bilgileri
            </CardTitle>
            <CardDescription>
              Hesabınla ilişkili temel bilgiler.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-lg border border-border bg-secondary/30 p-4">
              <div className="grid gap-3 text-sm md:grid-cols-2">
                <div>
                  <p className="text-xs text-muted-foreground">E-posta</p>
                  <p className="flex items-center gap-1 font-medium">
                    <Mail className="h-3.5 w-3.5" />
                    {user?.email ?? "—"}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Üyelik tarihi</p>
                  <p className="font-medium">{formatDate(user?.created_at)}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Giriş yöntemi</p>
                  <p className="font-medium capitalize">
                    {provider === "email" ? "E-posta" : provider}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Doğrulanmış</p>
                  <p className="flex items-center gap-1 font-medium">
                    <ShieldCheck className="h-3.5 w-3.5 text-primary" />
                    {user?.email_confirmed_at ? "Evet" : "Hayır"}
                  </p>
                </div>
              </div>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault()
                nameMutation.mutate()
              }}
              className="space-y-3"
            >
              <label className="block text-sm font-medium">İsim</label>
              <Input
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Adın Soyadın"
              />
              <Button
                type="submit"
                disabled={
                  nameMutation.isPending || fullName === displayNameInitial
                }
              >
                İsmi kaydet
              </Button>
            </form>
          </CardContent>
        </Card>

        {!isOAuth && (
          <Card>
            <CardHeader>
              <CardTitle>Şifre değiştir</CardTitle>
              <CardDescription>
                En az 6 karakter. Eskisini bilmen gerekmiyor — aktif oturum
                yeterli.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form
                onSubmit={(e) => {
                  e.preventDefault()
                  passwordMutation.mutate()
                }}
                className="space-y-3"
              >
                <Input
                  type="password"
                  placeholder="Yeni şifre"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  minLength={6}
                  autoComplete="new-password"
                />
                <Input
                  type="password"
                  placeholder="Yeni şifre (tekrar)"
                  value={passwordConfirm}
                  onChange={(e) => setPasswordConfirm(e.target.value)}
                  minLength={6}
                  autoComplete="new-password"
                />
                <Button
                  type="submit"
                  disabled={passwordMutation.isPending || !password}
                >
                  Şifreyi güncelle
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        <Card className="border-destructive/40">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-destructive">
              <Trash2 className="h-4 w-4" />
              Hesabı sil
            </CardTitle>
            <CardDescription>
              Hesabın ve tüm analizlerin kalıcı olarak silinir. Geri alınamaz.
            </CardDescription>
          </CardHeader>
          <CardContent>
            {confirmingDelete ? (
              <div className="space-y-3 rounded-lg border border-destructive/40 bg-destructive/5 p-4 text-sm">
                <p>
                  Emin misin? Tüm analiz geçmişin silinecek ve geri alınamaz.
                </p>
                <div className="flex gap-2">
                  <Button
                    variant="destructive"
                    onClick={() => deleteMutation.mutate()}
                    disabled={deleteMutation.isPending}
                  >
                    Evet, hesabımı sil
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => setConfirmingDelete(false)}
                    disabled={deleteMutation.isPending}
                  >
                    Vazgeç
                  </Button>
                </div>
              </div>
            ) : (
              <Button
                variant="destructive"
                onClick={() => setConfirmingDelete(true)}
              >
                Hesabı silmek istiyorum
              </Button>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
