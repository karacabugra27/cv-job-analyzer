import { Link, NavLink } from "react-router-dom"
import { Logo } from "./Logo"
import { ThemeToggle } from "./ThemeToggle"
import { cn } from "@/lib/utils"
import { useAuth } from "@/lib/auth"
import { Button } from "@/components/ui/button"

const navItems = [
  { to: "/", label: "Ana sayfa", end: true },
  { to: "/history", label: "Geçmiş analizler" },
]

export function Header() {
  const { user, signOut } = useAuth()

  return (
    <header className="border-b border-border bg-background/80 backdrop-blur sticky top-0 z-10">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link to="/">
          <Logo />
        </Link>

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

        <div className="flex items-center gap-3">
          {user && (
            <>
              <span className="hidden text-sm text-muted-foreground md:inline">
                {user.email}
              </span>
              <Button variant="ghost" size="sm" onClick={() => signOut()}>
                Çıkış
              </Button>
            </>
          )}
          <ThemeToggle />
        </div>
      </div>
    </header>
  )
}
