import { useEffect } from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { Toaster } from "sonner"
import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"
import { HomePage } from "@/pages/HomePage"
import { HistoryPage } from "@/pages/HistoryPage"
import { HistoryDetailPage } from "@/pages/HistoryDetailPage"
import { LoginPage } from "@/pages/LoginPage"
import { ProfilePage } from "@/pages/ProfilePage"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { ScrollToTop } from "@/components/ScrollToTop"
import { FeedbackButton } from "@/components/FeedbackButton"
import { AuthProvider } from "@/lib/auth"
import { useThemeStore, applyThemeClass } from "@/store/theme"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  const theme = useThemeStore((s) => s.theme)

  useEffect(() => {
    applyThemeClass(theme)
  }, [theme])

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <ScrollToTop />
          <div className="flex min-h-screen flex-col bg-background">
            <Header />
            <main className="flex-1">
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route
                  path="/"
                  element={
                    <ProtectedRoute>
                      <HomePage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/history"
                  element={
                    <ProtectedRoute>
                      <HistoryPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/history/:id"
                  element={
                    <ProtectedRoute>
                      <HistoryDetailPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <ProfilePage />
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </main>
            <Footer />
            <FeedbackButton />
          </div>
          <Toaster position="top-right" richColors theme={theme} />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
