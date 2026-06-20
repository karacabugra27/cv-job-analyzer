import { Moon, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useThemeStore } from "@/store/theme"

export function ThemeToggle() {
  const { theme, toggle } = useThemeStore()
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggle}
      aria-label="Tema değiştir"
    >
      {theme === "light" ? (
        <Moon className="h-4 w-4" />
      ) : (
        <Sun className="h-4 w-4" />
      )}
    </Button>
  )
}
