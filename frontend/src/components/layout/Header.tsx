import { useEffect, useRef, useState } from "react"
import { Link, NavLink, useLocation } from "react-router-dom"
import { LogOut, Menu, User, X } from "lucide-react"
import { Logo } from "./Logo"
import { ThemeToggle } from "./ThemeToggle"
import { cn } from "@/lib/utils"
import { useAuth } from "@/lib/auth"
import { Button } from "@/components/ui/button"

const navItems = [
  { to: "/", label: "Ana sayfa", end: true },
  { to: "/history", label: "Geçmiş analizler" },
]

function initialsFromEmail(email: string | null | undefined): string {
  if (!email) return "?"
  return email.slice(0, 2).toUpperCase()
}

export function Header() {
  const { session, user, signOut } = useAuth()
  const location = useLocation()
  const [menuOpen, setMenuOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const userMenuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setMenuOpen(false)
    setUserMenuOpen(false)
  }, [location.pathname])

  useEffect(() => {
    function onClickOutside(e: MouseEvent) {
      if (
        userMenuRef.current &&
        !userMenuRef.current.contains(e.target as Node)
      ) {
        setUserMenuOpen(false)
      }
    }
    document.addEventListener("mousedown", onClickOutside)
    return () => document.removeEventListener("mousedown", onClickOutside)
  }, [])

  if (location.pathname === "/login") return null
  if (!session) return null

  return (
    <header className="sticky top-0 z-20 border-b border-border bg-background/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-6 py-4">
        <Link to={session ? "/" : "/login"} className="shrink-0">
          <Logo />
        </Link>

        {session && (
          <nav className="hidden items-center gap-6 md:flex">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  cn(
                    "text-sm font-medium transition-colors hover:text-foreground",
                    isActive ? "text-foreground" : "text-muted-foreground"
                  )
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        )}

        <div className="flex items-center gap-2">
          <ThemeToggle />

          {session ? (
            <>
              <div ref={userMenuRef} className="relative hidden md:block">
                <button
                  type="button"
                  onClick={() => setUserMenuOpen((v) => !v)}
                  className="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
                  aria-label="Kullanıcı menüsü"
                >
                  {initialsFromEmail(user?.email)}
                </button>

                {userMenuOpen && (
                  <div className="absolute right-0 mt-2 w-56 overflow-hidden rounded-lg border border-border bg-popover shadow-lg">
                    <div className="border-b border-border px-3 py-2">
                      <p className="truncate text-xs text-muted-foreground">
                        Giriş yapıldı
                      </p>
                      <p className="truncate text-sm font-medium">
                        {user?.email}
                      </p>
                    </div>
                    <Link
                      to="/profile"
                      className="flex items-center gap-2 px-3 py-2 text-sm hover:bg-secondary"
                    >
                      <User className="h-4 w-4" />
                      Profil
                    </Link>
                    <button
                      type="button"
                      onClick={() => signOut()}
                      className="flex w-full items-center gap-2 px-3 py-2 text-sm text-destructive hover:bg-secondary"
                    >
                      <LogOut className="h-4 w-4" />
                      Çıkış yap
                    </button>
                  </div>
                )}
              </div>

              <Button
                variant="ghost"
                size="icon"
                className="md:hidden"
                onClick={() => setMenuOpen((v) => !v)}
                aria-label="Menü"
              >
                {menuOpen ? (
                  <X className="h-5 w-5" />
                ) : (
                  <Menu className="h-5 w-5" />
                )}
              </Button>
            </>
          ) : null}
        </div>
      </div>

      {session && menuOpen && (
        <div className="border-t border-border bg-background md:hidden">
          <nav className="mx-auto flex max-w-6xl flex-col px-6 py-3">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  cn(
                    "rounded-md px-2 py-2 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-secondary text-foreground"
                      : "text-muted-foreground hover:bg-secondary"
                  )
                }
              >
                {item.label}
              </NavLink>
            ))}
            <Link
              to="/profile"
              className="flex items-center gap-2 rounded-md px-2 py-2 text-sm text-muted-foreground hover:bg-secondary"
            >
              <User className="h-4 w-4" />
              Profil
            </Link>
            <div className="mt-2 border-t border-border pt-2">
              <p className="px-2 pb-2 text-xs text-muted-foreground">
                {user?.email}
              </p>
              <button
                type="button"
                onClick={() => signOut()}
                className="flex w-full items-center gap-2 rounded-md px-2 py-2 text-sm text-destructive hover:bg-secondary"
              >
                <LogOut className="h-4 w-4" />
                Çıkış yap
              </button>
            </div>
          </nav>
        </div>
      )}
    </header>
  )
}
